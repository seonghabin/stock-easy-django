from rest_framework import serializers

from .models import Term, UserTerm
from news.models import News


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]


class NewsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "publisher",
            "published_at",
        ]


class UserTermSerializer(serializers.ModelSerializer):
    term = TermSerializer(read_only=True)
    news = NewsSimpleSerializer(read_only=True)

    class Meta:
        model = UserTerm
        fields = [
            "id",
            "term",
            "news",
            "created_at",
        ]