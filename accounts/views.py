from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import *


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(request, username=email, password=password)

    if user is None:
        return Response(
            {"detail": "이메일 또는 비밀번호가 올바르지 않습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    login(request, user)

    return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"detail": "로그아웃되었습니다."}, status=status.HTTP_200_OK)
    
    
@ensure_csrf_cookie
@api_view(["GET", "PATCH"])
@permission_classes([AllowAny])
def me(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return Response(
                {
                    "isAuthenticated": True,
                    "user": UserSerializer(request.user).data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "isAuthenticated": False,
                "user": None,
            },
            status=status.HTTP_200_OK,
        )

    if not request.user.is_authenticated:
        return Response(
            {"detail": "로그인이 필요합니다."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    serializer = UserUpdateSerializer(
        request.user,
        data=request.data,
        partial=True,
    )

    if serializer.is_valid():
        user = serializer.save()

        if "password" in request.data:
            update_session_auth_hash(request, user)

        return Response(
            {
                "isAuthenticated": True,
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)