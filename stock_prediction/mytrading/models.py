from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Trader(AbstractUser):
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=False, blank=False)
    country = models.CharField(max_length=100, null=True, blank=True)
    is_subscriber = models.BooleanField(default=False)
    interface_language = models.CharField(max_length=10, null=True, blank=True)
    # phone number, profile picture, dob, country, is_subscriber, preferred_language 



class Stock(models.Model):
    name = models.CharField(max_length=16)
    ticker = models.CharField(max_length=12)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)





