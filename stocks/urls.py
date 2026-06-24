from django.urls import path
from . import views


app_name = "stocks"

urlpatterns = [
    path("", views.stock_list),
    path("interests/", views.interest_stock_list_create),
    path("interests/<int:pk>/", views.interest_stock_delete),
    path("interests/themes/", views.recommended_theme_list),
]