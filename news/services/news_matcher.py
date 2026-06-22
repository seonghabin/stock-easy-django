"""
News 매칭 파이프라인

1차 구현
뉴스에서 직접 언급된 기업명 매칭
→ NewsStock 저장
→ 테마 페이지에서 Theme → StockTheme → NewsStock → News 조회

2차 AI 보완 (TODO)
기업명이 직접 안 나온 뉴스
예: 국고채, 금리, 환율, 원전 정책, 방산 수출, AI 인프라
→ AI가 관련 가능 기업 추론
→ NewsStock 보완 저장
"""

from news.models import NewsStock
from stocks.models import Stock

def match_news_stocks(news):
    text = f"{news.title} {news.content}"

    candidates = []

    for stock in Stock.objects.all():
        stock_name = stock.stock_name

        if not stock_name:
            continue

        if stock_name in text:
            candidates.append(stock)

    filtered_stocks = []

    for stock in candidates:
        # sk하이닉스 기사에 대해 sk와 이닉스가 들어가는 것을 막기 위함
        stock_name = stock.stock_name
        is_part_of_longer_name = False

        for other_stock in candidates:
            other_name = other_stock.stock_name

            if stock.id == other_stock.id:
                continue

            if stock_name in other_name and len(stock_name) < len(other_name):
                is_part_of_longer_name = True
                break

        if not is_part_of_longer_name:
            filtered_stocks.append(stock)

    matched_stocks = []

    for stock in filtered_stocks:
        NewsStock.objects.get_or_create(
            news=news,
            stock=stock,
        )
        matched_stocks.append(stock)

    return matched_stocks