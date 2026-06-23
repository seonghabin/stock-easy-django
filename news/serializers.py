from rest_framework import serializers
from .models import News, NewsStock
from analyses.serializers import AiAnalysisSerializer


class NewsStockSerializer(serializers.ModelSerializer):
    stock_id = serializers.IntegerField(source="stock.id", read_only=True)
    stock_name = serializers.CharField(source="stock.stock_name", read_only=True)
    stock_code = serializers.CharField(source="stock.stock_code", read_only=True)

    class Meta:
        model = NewsStock
        fields = [
            "stock_id",
            "stock_name",
            "stock_code",
        ]


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "author",
            "publisher",
            "published_at",
            "thumbnail_url",
            "url"
        ]

class NewsDetailSerializer(serializers.ModelSerializer):
    ai_analysis = AiAnalysisSerializer(read_only=True)
    news_stocks = NewsStockSerializer(many=True, read_only=True)
    class Meta:

        model = News
        fields = [
            "id",
            "title",
            "url",
            "description",
            "content",
            "author",
            "publisher",
            "published_at",
            "thumbnail_url",
            
            "ai_analysis",
            "news_stocks",
        ]