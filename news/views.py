from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import News
from .serializers import NewsListSerializer


@api_view(["GET"])
def news_list(request):
    news_qs = News.objects.all().order_by("-published_at")
    serializer = NewsListSerializer(news_qs, many=True)
    return Response(serializer.data)