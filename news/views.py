from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import *
from stocks.models import StockTheme
from .serializers import *

from analyses.services import get_or_create_ai_analysis

from rest_framework import status
from rest_framework.permissions import IsAuthenticated


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

    get_or_create_ai_analysis(news)

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


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def saved_news_list_create(request):
    if request.method == "GET":
        saved_news_qs = (
            SavedNews.objects.filter(user=request.user)
            .select_related("news")
            .order_by("created_at")
        )

        serializer = SavedNewsSerializer(saved_news_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    news_id = request.data.get("news_id")

    if not news_id:
        return Response(
            {"detail": "news_id는 필수입니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        news = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return Response(
            {"detail": "뉴스를 찾을 수 없습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    saved_news, created = SavedNews.objects.get_or_create(
        user=request.user,
        news=news,
    )

    if not created:
        return Response(
            {"detail": "이미 저장된 뉴스입니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = SavedNewsSerializer(saved_news)
    return Response(serializer.data, status=status.HTTP_201_CREATED)