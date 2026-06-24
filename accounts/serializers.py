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
        
class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=False,
    )

    class Meta:
        model = User
        fields = ("email", "nickname", "password")
        extra_kwargs = {
            "email": {"required": False},
            "nickname": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def validate_email(self, value):
        user = self.instance

        if (
            value
            and User.objects.exclude(id=user.id).filter(email=value).exists()
        ):
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")

        return value

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance