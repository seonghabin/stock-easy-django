from django.db import models


class Stock(models.Model):
    class Market(models.TextChoices):
        KOSPI = "KOSPI", "유가"
        KOSDAQ = "KOSDAQ", "코스닥"
        KONEX = "KONEX", "코넥스"

    stock_code = models.CharField(max_length=20, unique=True) #종목코드
    stock_name = models.CharField(max_length=100) #회사명
    market = models.CharField(max_length=10, choices=Market.choices)
    industry = models.CharField(max_length=100, blank=True, null=True) #업종
    main_product = models.TextField(blank=True, null=True) #주요제품

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stock_name}({self.stock_code})"


class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class StockTheme(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="theme_relations")
    theme = models.ForeignKey(Theme,on_delete=models.CASCADE, related_name="stock_relations")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["stock", "theme"],name="unique_stock_theme")
        ]

    def __str__(self):
        return f"{self.stock.stock_name} - {self.theme.name}"