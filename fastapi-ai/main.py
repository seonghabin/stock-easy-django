from fastapi import FastAPI
from schemas import NewsRequest, NewsResponse
from services.ai_service import analyze_news_with_ai



app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

    
@app.post("/analyze", response_model=NewsResponse)
def analyze(req: NewsRequest):
    return analyze_news_with_ai(req.title, req.content)


# @app.post("/analyze", response_model=NewsResponse)
# def analyze(req: NewsRequest):

#     # AI 대신 mock 데이터 테스트
#     return {
#         "rewritten_content": f"[AI 요약] {req.title}",
#         "sentiment": "neutral",
#         "impact_score": 0.72,
#         "impact_reason": "시장 영향 중간 수준",
#         "difficult_terms": ["반도체", "금리"],
#         "check_points": ["실적 확인 필요", "수급 변화"]
#     }