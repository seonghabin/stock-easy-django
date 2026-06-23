from rest_framework import serializers
from .models import User


class SignupSerializer(serializers.ModelSerializer): #입력 담당
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "nickname")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer): #출력 담당
    class Meta:
        model = User
        fields = ("id", "email", "nickname")