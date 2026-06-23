from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    
    
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def comment_update(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {"detail": "댓글을 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if comment.user != request.user:
        return Response(
            {"detail": "댓글 작성자만 수정할 수 있습니다."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = CommentSerializer(comment, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def comment_list(request, news_id):
    try:
        news = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return Response(
            {"detail": "뉴스를 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND,
        )

    comments = Comment.objects.filter(news=news).select_related("user")
    serializer = CommentSerializer(comments, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)