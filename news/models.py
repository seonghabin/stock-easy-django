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

    
class NewsStock(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="news_stocks")
    stock = models.ForeignKey("stocks.Stock", on_delete=models.CASCADE,related_name="news_stocks")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["news", "stock"], name="unique_news_stock")]

    def __str__(self):
        return f"{self.news.title} - {self.stock.stock_name}"
    
    
class NewsTheme(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="news_themes")
    theme = models.ForeignKey("stocks.Theme", on_delete=models.CASCADE, related_name="news_themes")
    relation_reason = models.TextField(blank=True, null=True)
    confidence_score = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["news", "theme"], name="unique_news_theme")]

    def __str__(self):
        return f"{self.news.title} - {self.theme.name}"

class SavedNews(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="saved_news",)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="saved_news")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "news"], name="unique_user_saved_news")
        ]

    def __str__(self):
        return f"{self.user.email} - {self.news.title}"