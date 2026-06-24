from django.urls import path
from . import views


app_name = "terms"

urlpatterns = [
    path("my/", views.my_term_list_create),
    path("my/<int:pk>/", views.my_term_delete),
]