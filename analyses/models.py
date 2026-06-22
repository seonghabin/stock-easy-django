from django.db import models
from news.models import News

class AiAnalysis(models.Model):
    news = models.OneToOneField(News, on_delete=models.CASCADE, related_name="ai_analysis")

    rewritten_content = models.TextField()   # 뉴스 재작성

    sentiment = models.CharField(max_length=20)    # 감정분석: positive / negative / neutral
    impact_score = models.FloatField()
    impact_reason = models.TextField()

    difficult_terms = models.JSONField(null=True, blank=True)   # 어려운 용어 분석
    check_points = models.JSONField(null=True, blank=True)   # 투자 포인트

    status = models.CharField(max_length=20,default="pending")    # 상태관리 pending / success / failed
    error_message = models.TextField(null=True, blank=True)

    analyzed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)