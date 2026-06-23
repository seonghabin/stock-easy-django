from pydantic import BaseModel
from typing import List, Optional


# 1. 요청 스키마 (Django → FastAPI)
class NewsRequest(BaseModel):
    news_id: int
    title: str
    content: str


class Highlight(BaseModel):
    sentence: str
    reason: str


class DifficultTerm(BaseModel):
    term: str
    explanation: str


# 2. 응답 스키마 (FastAPI → Django)
class NewsResponse(BaseModel):
    rewritten_content: str
    sentiment: str
    sentiment_reason: str
    impact_score: float
    impact_reason: str
    highlight: Optional[List[Highlight]] = None
    difficult_terms: Optional[List[DifficultTerm]] = None
    check_points: Optional[List[str]] = None