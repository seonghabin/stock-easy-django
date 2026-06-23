from rest_framework import serializers
from .models import Stock, InterestStock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = [
            "id",
            "stock_code",
            "stock_name",
            "market",
            "industry",
            "main_product",
        ]


class InterestStockSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)

    class Meta:
        model = InterestStock
        fields = [
            "id",
            "stock",
            "created_at",
        ]