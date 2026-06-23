from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/stocks/", include("stocks.urls")),
    path("api/v1/news/", include("news.urls")),
    path("api/v1/analyses/", include("analyses.urls")),
    path("api/v1/comments/", include("comments.urls")),

]