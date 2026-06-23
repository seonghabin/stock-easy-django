from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from news.models import News

from .models import Comment
from .serializers import CommentSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def comment_create(request, news_id):
    try:
        news = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return Response(
            {"detail": "뉴스를 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = CommentSerializer(data=request.data)

    if serializer.is_valid():
        comment = serializer.save(
            news=news,
            user=request.user,
        )

        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )