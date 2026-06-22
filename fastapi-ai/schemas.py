from pydantic import BaseModel
from typing import List, Optional


# 1. 요청 스키마 (Django → FastAPI)
class NewsRequest(BaseModel):
    news_id: int
    title: str
    content: str

# 2. 응답 스키마 (FastAPI → Django)
class NewsResponse(BaseModel):
    rewritten_content: str
    sentiment: str
    impact_score: float
    impact_reason: str
    difficult_terms: Optional[list] = None
    check_points: Optional[list] = None