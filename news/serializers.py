from rest_framework import serializers
from .models import News
from analyses.serializers import AiAnalysisSerializer

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "author",
            "publisher",
            "published_at",
            "thumbnail_url",
            "url"
        ]

class NewsDetailSerializer(serializers.ModelSerializer):
    ai_analysis = AiAnalysisSerializer(read_only=True)
    
    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "url",
            "description",
            "content",
            "author",
            "publisher",
            "published_at",
            "thumbnail_url",
            
            "ai_analysis",
        ]