import requests

FASTAPI_ANALYZE_URL = "http://127.0.0.1:8001/analyze"


def request_ai_analysis(news):
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