from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import News
from .serializers import *


@api_view(["GET"])
def news_list(request):
    news_qs = News.objects.all().order_by("-published_at")
    serializer = NewsListSerializer(news_qs, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def news_detail(request, news_id):
    try:
        news = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return Response({"detail": "Not found"}, status=404)

    serializer = NewsDetailSerializer(news)
    return Response(serializer.data)