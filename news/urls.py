from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("", views.news_list),
    path("<int:news_id>/", views.news_detail),
]