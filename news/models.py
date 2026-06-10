from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    description = models.TextField()
    content = models.TextField()
    author = models.CharField(max_length=100, blank=True)
    publisher = models.CharField(max_length=50)
    published_at = models.DateTimeField()
    collected_at = models.DateTimeField(auto_now_add=True)
    thumbnail_url = models.URLField(blank=True, null=True)

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