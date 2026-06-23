from django.urls import path
from . import views


app_name = "stocks"

urlpatterns = [
    path("", views.stock_list),
    path("interests/", views.interest_stock_list_create),
]