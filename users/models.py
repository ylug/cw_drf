from django.db import models
from django.contrib.auth.models import AbstractUser


NULLABLE = {"null": True, "blank": True}

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(max_length=35, verbose_name="телефон", **NULLABLE)
    city = models.CharField(max_length=50, verbose_name="город", **NULLABLE)
    avatar = models.ImageField(upload_to="users/", verbose_name="аватар", **NULLABLE)
    chat_id = models.CharField(unique=True, max_length=50, verbose_name="телеграмм", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
