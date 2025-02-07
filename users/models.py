# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Модель пользователя, расширяющая стандартную User"""
    email = models.EmailField(unique=True)  # Делаем email обязательным

    def __str__(self):
        return self.username
