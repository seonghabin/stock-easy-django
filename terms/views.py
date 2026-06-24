from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from news.models import News
from .models import Term, UserTerm
from .serializers import UserTermSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def my_term_list_create(request):
    if request.method == "GET":
        user_terms = (
            UserTerm.objects.filter(user=request.user)
            .select_related("term", "news")
            .order_by("created_at")
        )

        serializer = UserTermSerializer(user_terms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    term_name = request.data.get("term")
    explanation = request.data.get("explanation")
    news_id = request.data.get("news_id")

    if not term_name:
        return Response(
            {"detail": "term은 필수입니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not explanation:
        return Response(
            {"detail": "explanation은 필수입니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not news_id:
        return Response(
            {"detail": "news_id는 필수입니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        news = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return Response(
            {"detail": "뉴스를 찾을 수 없습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    term, _ = Term.objects.get_or_create(
        name=term_name,
        defaults={
            "description": explanation,
        },
    )

    user_term, created = UserTerm.objects.get_or_create(
        user=request.user,
        term=term,
        news=news,
    )

    if not created:
        return Response(
            {"detail": "이미 해당 뉴스에서 저장된 용어입니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = UserTermSerializer(user_term)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def my_term_delete(request, pk):
    try:
        user_term = UserTerm.objects.get(
            id=pk,
            user=request.user,
        )
    except UserTerm.DoesNotExist:
        return Response(
            {"detail": "저장된 용어를 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND,
        )

    user_term.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)