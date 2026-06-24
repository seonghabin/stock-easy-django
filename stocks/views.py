from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Stock, InterestStock, Theme
from .serializers import StockSerializer, InterestStockSerializer, ThemeSerializer


@api_view(["GET"])
def stock_list(request):
    search = request.GET.get("search")

    stocks = Stock.objects.all().order_by("stock_name")

    if search:
        stocks = stocks.filter(
            Q(stock_name__icontains=search) |
            Q(stock_code__icontains=search)
        )

    serializer = StockSerializer(stocks, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def interest_stock_list_create(request):
    if request.method == "GET":
        interest_stocks = InterestStock.objects.filter(
            user=request.user
        ).select_related("stock")

        serializer = InterestStockSerializer(interest_stocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    stock_id = request.data.get("stock_id")

    if not stock_id:
        return Response(
            {"detail": "stock_id는 필수입니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        stock = Stock.objects.get(id=stock_id)
    except Stock.DoesNotExist:
        return Response(
            {"detail": "존재하지 않는 종목입니다."},
            status=status.HTTP_404_NOT_FOUND,
        )

    interest_stock, created = InterestStock.objects.get_or_create(
        user=request.user,
        stock=stock,
    )

    if not created:
        return Response(
            {"detail": "이미 등록된 관심종목입니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = InterestStockSerializer(interest_stock)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def interest_stock_delete(request, pk):
    try:
        interest_stock = InterestStock.objects.get(
            id=pk,
            user=request.user,
        )
    except InterestStock.DoesNotExist:
        return Response(
            {"detail": "관심종목을 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND,
        )

    interest_stock.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def recommended_theme_list(request):
    interest_stocks = InterestStock.objects.filter(
        user=request.user
    ).select_related("stock").order_by("created_at")

    themes = []
    seen_theme_ids = set()

    for interest_stock in interest_stocks:
        stock_themes = Theme.objects.filter(
            stock_relations__stock=interest_stock.stock
        ).order_by("name")[:5]

        for theme in stock_themes:
            if theme.id not in seen_theme_ids:
                themes.append(theme)
                seen_theme_ids.add(theme.id)

    serializer = ThemeSerializer(themes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)