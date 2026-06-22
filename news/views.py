from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from stocks.models import StockTheme
from .serializers import *


@api_view(["GET"])
def news_list(request):
    news_qs = News.objects.all().order_by("-published_at")
    serializer = NewsSerializer(news_qs, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def news_detail(request, news_id):
    try:
        news = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return Response({"detail": "Not found"}, status=404)

    serializer = NewsDetailSerializer(news)
    return Response(serializer.data)

@api_view(["GET"])
def stock_news(request, stock_id):
    news_qs = NewsStock.objects.filter(stock_id=stock_id).select_related("news").order_by("-news__published_at")
    news_list = [ns.news for ns in news_qs]
    serializer = NewsSerializer(news_list, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def theme_news(request, theme_id):
    # 1. 테마에 속한 종목 조회
    stock_ids = StockTheme.objects.filter(theme_id=theme_id).values_list("stock_id", flat=True)
    # 2. 해당 종목이 포함된 뉴스 ID 조회
    news_ids = NewsStock.objects.filter(stock_id__in=stock_ids).values_list("news_id", flat=True)
    # 3. 뉴스 조회
    news_qs = News.objects.filter(id__in=news_ids).order_by("-published_at").distinct()
    
    serializer = NewsSerializer(news_qs, many=True)
    return Response(serializer.data)