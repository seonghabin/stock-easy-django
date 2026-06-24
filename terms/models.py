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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "term"],name="unique_user_term")
        ]

    def __str__(self):
        return f"{self.user} - {self.term.name}"