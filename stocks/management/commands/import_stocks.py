import pandas as pd
from pathlib import Path

from django.core.management.base import BaseCommand
from stocks.models import Stock


class Command(BaseCommand):
    help = "상장법인목록 엑셀 데이터를 Stock 테이블에 저장합니다."

    def handle(self, *args, **options):
        file_path = Path("stocks/data/listed_companies.xls")

        tables = pd.read_html(file_path, encoding="euc-kr")
        df = tables[0]

        market_map = {
            "유가": Stock.Market.KOSPI,
            "코스닥": Stock.Market.KOSDAQ,
            "코넥스": Stock.Market.KONEX,
        }

        stocks = []

        for _, row in df.iterrows():
            market = market_map.get(row["시장구분"])

            if market is None:
                self.stdout.write(
                    self.style.WARNING(f"알 수 없는 시장구분: {row['시장구분']}")
                )
                continue

            stock = Stock(
                stock_code=str(row["종목코드"]).zfill(6),
                stock_name=row["회사명"],
                market=market,
                industry=row["업종"] if pd.notna(row["업종"]) else None,
                main_product=row["주요제품"] if pd.notna(row["주요제품"]) else None,
            )
            stocks.append(stock)

        Stock.objects.bulk_create(stocks, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(f"{len(stocks)}개 종목 데이터 저장 완료")
        )