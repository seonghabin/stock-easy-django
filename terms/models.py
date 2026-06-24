from django.conf import settings
from django.db import models


class Term(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserTerm(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_terms")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="saved_users")
    news = models.ForeignKey("news.News", on_delete=models.CASCADE, related_name="user_terms", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "term", "news"], name="unique_user_term_news",)
        ]

    def __str__(self):
        return f"{self.user} - {self.term}"