from django.db import models
from users.models import CustomUser
# Create your models here.


class Reservation(models.Model):
    day = models.CharField(max_length=2)
    month = models.CharField(max_length=2)
    year = models.CharField(max_length=4)
    start_hour = models.CharField(max_length=2)
    start_minute = models.CharField(max_length=2)
    end_hour = models.CharField(max_length=2)
    end_minute = models.CharField(max_length=2)
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor')
