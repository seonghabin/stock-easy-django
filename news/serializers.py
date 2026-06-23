from rest_framework import serializers
from stocks.models import Stock
from .models import News
from analyses.serializers import AiAnalysisSerializer


class RelatedStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = [
            "id",
            "stock_code",
            "stock_name",
        ]


class NewsSerializer(serializers.ModelSerializer):
    related_stocks = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "author",
            "publisher",
            "published_at",
            "thumbnail_url",
            "url",

            "related_stocks",
        ]

    def get_related_stocks(self, obj):
        stocks = Stock.objects.filter(news_stocks__news=obj)
        return RelatedStockSerializer(stocks, many=True).data


class NewsDetailSerializer(serializers.ModelSerializer):
    ai_analysis = AiAnalysisSerializer(read_only=True)
    related_stocks = serializers.SerializerMethodField()

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
            "related_stocks",
        ]

    def get_related_stocks(self, obj):
        stocks = Stock.objects.filter(news_stocks__news=obj)
        return RelatedStockSerializer(stocks, many=True).data