from rest_framework import serializers
from .models import AiAnalysis


class AiAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiAnalysis
        fields = "__all__"