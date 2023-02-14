from django.db import models
from django.contrib.auth.models import User
from stock_prediction.settings import STRIPE_API_KEY
import stripe


class UserAccountProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    stripe_customer_id = models.CharField(max_length=120)
    

    