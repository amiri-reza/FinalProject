from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django_countries.fields import CountryField
from django.utils import timezone


class Stock(models.Model):
    name = models.CharField(max_length=16)
    ticker = models.CharField(max_length=12)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Trader(AbstractUser):
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(blank=False, default=timezone.now())
    country = CountryField()
    is_subscriber = models.BooleanField(default=False)
    interface_language = models.CharField(max_length=10, null=True, blank=True)


#     # phone number, profile picture, dob, country, is_subscriber, preferred_language
