from django.urls import path
from . import views


app_name = "comments"

urlpatterns = [
    path("news/<int:news_id>/", views.comment_list),
    path("news/<int:news_id>/create/", views.comment_create),
    path("<int:comment_id>/", views.comment_update),
    path("<int:comment_id>/", views.comment_delete),
]