from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Stock
from .serializers import StockSerializer


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