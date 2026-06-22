from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
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