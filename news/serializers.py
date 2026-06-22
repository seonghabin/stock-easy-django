from rest_framework import serializers
from .models import News


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "author",
            "publisher",
            "published_at",
            "thumbnail_url",
            "url"
        ]