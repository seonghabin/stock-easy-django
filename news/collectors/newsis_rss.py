"""
뉴시스 RSS 수집기
- URL: https://www.newsis.com/RSS/bank.xml (금융)
- feedparser로 파싱 후 Django ORM으로 저장
- url UNIQUE 제약으로 중복 저장 방지
"""

import logging
import re
from datetime import datetime
from email.utils import parsedate_to_datetime

import feedparser
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# 뉴시스 분야별 RSS URL (나중에 섹션 확장할 때 여기에 추가)
NEWSIS_RSS_FEEDS = {
    '금융': 'https://www.newsis.com/RSS/bank.xml',
    # '경제': 'https://www.newsis.com/RSS/economy.xml',
    # '산업': 'https://www.newsis.com/RSS/industry.xml',
}


def strip_html(html_text: str) -> str:
    """HTML 태그 제거 후 순수 텍스트 반환"""
    if not html_text:
        return ''
    soup = BeautifulSoup(html_text, 'html.parser')
    text = soup.get_text(separator=' ')
    # 연속 공백/개행 정리
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_thumbnail(entry) -> str | None:
    """RSS entry에서 썸네일 URL 추출"""
    # media:thumbnail 태그
    if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
        return entry.media_thumbnail[0].get('url')
    # enclosure (이미지)
    if hasattr(entry, 'enclosures') and entry.enclosures:
        for enc in entry.enclosures:
            if enc.get('type', '').startswith('image/'):
                return enc.get('url') or enc.get('href')
    # description 안의 img 태그
    description = getattr(entry, 'description', '') or ''
    soup = BeautifulSoup(description, 'html.parser')
    img = soup.find('img')
    if img:
        return img.get('src')
    return None


def parse_published_at(entry) -> datetime | None:
    """RSS published 날짜 파싱"""
    # feedparser가 파싱한 struct_time → datetime
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        import calendar
        return datetime.utcfromtimestamp(
            calendar.timegm(entry.published_parsed)
        ).replace(tzinfo=__import__('datetime').timezone.utc)
    # 문자열로 직접 있는 경우
    published_str = getattr(entry, 'published', None)
    if published_str:
        try:
            return parsedate_to_datetime(published_str)
        except Exception:
            pass
    return None


def fetch_and_save(section: str, rss_url: str) -> dict:
    """
    RSS 수집 → 파싱 → DB 저장
    Returns: {'created': int, 'skipped': int, 'errors': int}
    """
    # Django 모델은 이 함수가 호출될 때 import (management command에서 Django setup 이후)
    from news.models import News

    stats = {'created': 0, 'skipped': 0, 'errors': 0}

    try:
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f'[{section}] RSS 요청 실패: {e}')
        stats['errors'] += 1
        return stats

    feed = feedparser.parse(response.content)

    if feed.bozo:
        logger.warning(f'[{section}] RSS 파싱 경고: {feed.bozo_exception}')

    for entry in feed.entries:
        try:
            url = entry.get('link', '').strip()
            if not url:
                continue

            # 중복 체크 (url UNIQUE)
            if News.objects.filter(url=url).exists():
                stats['skipped'] += 1
                continue

            title = entry.get('title', '').strip()
            description = entry.get('description', '') or entry.get('summary', '')
            content = strip_html(description)
            author = entry.get('author', '').strip() or None
            published_at = parse_published_at(entry)
            thumbnail_url = extract_thumbnail(entry)

            News.objects.create(
                title=title,
                url=url,
                description=description,
                content=content,
                author=author,
                publisher='뉴시스',
                published_at=published_at,
                thumbnail_url=thumbnail_url,
            )
            stats['created'] += 1
            logger.debug(f'[{section}] 저장: {title}')

        except Exception as e:
            logger.error(f'[{section}] 기사 저장 실패: {e} / entry={entry.get("link")}')
            stats['errors'] += 1

    return stats


def collect_all() -> dict:
    """
    등록된 모든 RSS 피드 수집
    Returns: 섹션별 통계 dict
    """
    result = {}
    for section, url in NEWSIS_RSS_FEEDS.items():
        logger.info(f'[{section}] 수집 시작: {url}')
        stats = fetch_and_save(section, url)
        result[section] = stats
        logger.info(
            f'[{section}] 완료 — 신규: {stats["created"]}, '
            f'중복: {stats["skipped"]}, 오류: {stats["errors"]}'
        )
    return result
