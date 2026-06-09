import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from stocks.models import Stock, Theme, StockTheme


class Command(BaseCommand):
    help = "네이버 금융 테마별 구성종목을 수집합니다."

    BASE_URL = "https://finance.naver.com"
    THEME_LIST_URL = "https://finance.naver.com/sise/theme.naver"

    def add_arguments(self, parser):
        parser.add_argument(
            "--save",
            action="store_true",
            help="수집 결과를 Theme, StockTheme 테이블에 저장합니다.",
        )
        parser.add_argument(
            "--max-page",
            type=int,
            default=7,
            help="수집할 테마 목록 최대 페이지 수입니다.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="테스트용으로 수집할 테마 개수를 제한합니다.",
        )

    def handle(self, *args, **options):
        save = options["save"]
        max_page = options["max_page"]
        limit = options["limit"]

        themes = self.get_theme_list(max_page=max_page)

        if limit:
            themes = themes[:limit]

        self.stdout.write(f"테마 {len(themes)}개 수집 시작")

        total_relations = 0
        failed_stocks = []

        for index, theme in enumerate(themes, start=1):
            theme_name = theme["name"]
            theme_url = theme["url"]

            stocks = self.get_theme_stocks(theme_url)

            self.stdout.write(f"[{index}/{len(themes)}] {theme_name} - {len(stocks)}개 종목")

            for stock_data in stocks:
                stock_code = stock_data["stock_code"]
                stock_name = stock_data["stock_name"]

                if not save:
                    self.stdout.write(f"  - {stock_name}({stock_code})")
                    continue

                theme_obj, _ = Theme.objects.get_or_create(name=theme_name)

                try:
                    stock_obj = Stock.objects.get(stock_code=stock_code)
                except Stock.DoesNotExist:
                    failed_stocks.append(f"{stock_name}({stock_code})")
                    continue

                StockTheme.objects.get_or_create(
                    stock=stock_obj,
                    theme=theme_obj,
                )
                total_relations += 1

            time.sleep(0.3)

        if save:
            self.stdout.write(self.style.SUCCESS(f"StockTheme 저장 완료: {total_relations}개"))

            if failed_stocks:
                self.stdout.write(self.style.WARNING(f"매핑 실패 종목: {len(failed_stocks)}개"))
                for item in failed_stocks[:20]:
                    self.stdout.write(f"  - {item}")

        else:
            self.stdout.write(self.style.WARNING("dry-run 완료: DB에는 저장하지 않았습니다."))
            self.stdout.write("저장하려면 --save 옵션을 붙이세요.")

    def get_theme_list(self, max_page):
        themes = []

        for page in range(1, max_page + 1):
            url = f"{self.THEME_LIST_URL}?page={page}"

            response = requests.get(url, headers=self.get_headers(), timeout=10)
            response.raise_for_status()
            response.encoding = "euc-kr"

            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.select("a[href*='sise_group_detail.naver?type=theme']"):
                theme_name = link.get_text(strip=True)
                href = link.get("href")

                if not theme_name or not href:
                    continue

                theme_url = urljoin(self.BASE_URL, href)

                themes.append({
                    "name": theme_name,
                    "url": theme_url,
                })

            time.sleep(0.3)

        return self.remove_duplicate_themes(themes)

    def get_theme_stocks(self, theme_url):
        response = requests.get(theme_url, headers=self.get_headers(), timeout=10)
        response.raise_for_status()
        response.encoding = "euc-kr"

        soup = BeautifulSoup(response.text, "html.parser")

        stocks = []

        for link in soup.select("a[href*='item/main.naver?code=']"):
            stock_name = link.get_text(strip=True)
            href = link.get("href")

            match = re.search(r"code=(\w+)", href)

            if not match or not stock_name:
                continue

            stock_code = match.group(1)

            stocks.append({
                "stock_name": stock_name,
                "stock_code": stock_code,
            })

        return self.remove_duplicate_stocks(stocks)

    def remove_duplicate_themes(self, themes):
        seen = set()
        result = []

        for theme in themes:
            key = theme["url"]

            if key in seen:
                continue

            seen.add(key)
            result.append(theme)

        return result

    def remove_duplicate_stocks(self, stocks):
        seen = set()
        result = []

        for stock in stocks:
            key = stock["stock_code"]

            if key in seen:
                continue

            seen.add(key)
            result.append(stock)

        return result

    def get_headers(self):
        return {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/148.0.0.0 Safari/537.36"
            )
        }