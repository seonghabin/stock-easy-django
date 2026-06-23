import requests
from django.utils import timezone
from .models import AiAnalysis

FASTAPI_ANALYZE_URL = "http://127.0.0.1:8001/analyze"


def request_ai_analysis(news): #FastAPI 호출만 담당
    response = requests.post(
        FASTAPI_ANALYZE_URL,
        json={
            "news_id": news.id,
            "title": news.title,
            "content": news.content,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_or_create_ai_analysis(news): #실제 news/view/news_detail 에서 사용할 상위 함수
    try: #캐싱체크
        return news.ai_analysis
    except AiAnalysis.DoesNotExist:
        pass

    try:
        data = request_ai_analysis(news)

        return AiAnalysis.objects.create(
            news=news,
            rewritten_content=data["rewritten_content"],
            sentiment=data["sentiment"],
            impact_score=data["impact_score"],
            impact_reason=data["impact_reason"],
            difficult_terms=data.get("difficult_terms"),
            check_points=data.get("check_points"),
            status="success",
            analyzed_at=timezone.now(),
        )

    except Exception as e:
        return AiAnalysis.objects.create(
            news=news,
            rewritten_content="",
            sentiment="neutral",
            impact_score=0.0,
            impact_reason="",
            difficult_terms=None,
            check_points=None,
            status="failed",
            error_message=str(e),
            analyzed_at=timezone.now(),
        )