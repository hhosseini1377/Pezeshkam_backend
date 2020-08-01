from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    field = models.CharField(blank=True, max_length=20, default="پزشک عمومی")
    phone_number = models.CharField(blank= True, max_length=10)

    def __str__(self):
        return self.username
