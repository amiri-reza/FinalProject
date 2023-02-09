from django.db import models
from django.contrib.auth.models import User


class Stock(models.Model):
    name = models.CharField(max_length=16)
    ticker = models.CharField(max_length=12)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
