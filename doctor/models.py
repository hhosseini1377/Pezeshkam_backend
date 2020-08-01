from django.db import models

# Create your models here.

class Doctor(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    speciality = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
