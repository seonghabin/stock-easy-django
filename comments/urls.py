from django.urls import path
from . import views


app_name = "comments"

urlpatterns = [
    path("news/<int:news_id>/", views.comment_create),
]