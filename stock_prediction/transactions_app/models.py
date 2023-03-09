from django.db import models
from django.contrib.auth.models import User
from stock_prediction.settings import STRIPE_API_KEY
import stripe
from django.conf import settings


class UserAccountProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=120)


class TraderCoins(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coins = models.IntegerField()


class Purchase(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
