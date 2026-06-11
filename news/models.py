from django.db import models


class News(models.Model):
    title = models.CharField(max_length=500)
    url = models.URLField(max_length=1000, unique=True)
    description = models.TextField(blank=True, null=True)   # RSS 원문
    content = models.TextField(blank=True, null=True)       # html 제거한 본문 텍스트
    author = models.CharField(max_length=100, blank=True, null=True)  # 기자 이름
    publisher = models.CharField(max_length=100, default='뉴시스')    # 보도사
    published_at = models.DateTimeField(blank=True, null=True)
    collected_at = models.DateTimeField(auto_now_add=True)
    thumbnail_url = models.URLField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'news'
        ordering = ['-published_at']

    def __str__(self):
        return self.title
