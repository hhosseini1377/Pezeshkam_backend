from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    field = models.CharField(blank=True, max_length=20, default="پزشک عمومی")
    phone_number = models.CharField(blank=True, max_length=12)
    is_doctor = models.BooleanField(default=True)
    avatar = models.ImageField(default='default_avatar.png')
    name = models.CharField(max_length=20, default="ناشناس")

    def __str__(self):
        return self.username
