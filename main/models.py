# main/models

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    input_text = models.TextField(max_length=1000)
    translated_text = models.TextField()
    comment = models.TextField(max_length=1000, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Добавляем

    def __str__(self):
        return f"Chat by {self.user.username} at {self.timestamp}"
