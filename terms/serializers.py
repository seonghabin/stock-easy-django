from rest_framework import serializers

from .models import Term, UserTerm


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


class UserTermSerializer(serializers.ModelSerializer):
    term = TermSerializer(read_only=True)

    class Meta:
        model = UserTerm
        fields = [
            "id",
            "term",
            "created_at",
        ]