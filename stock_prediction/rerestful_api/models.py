from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Signal(models.Model):
    buy_emas = ArrayField(models.FloatField(), blank=True, default=list)
    sell_emas = ArrayField(models.FloatField(), blank=True, default=list)
    buy_smas = ArrayField(models.FloatField(), blank=True, default=list)
    sell_smas = ArrayField(models.FloatField(), blank=True, default=list)

    buy_ema_10_25 = ArrayField(models.FloatField(), blank=True, default=list)
    sell_ema_10_25 = ArrayField(models.FloatField(), blank=True, default=list)
    buy_ema_25_50 = ArrayField(models.FloatField(), blank=True, default=list)
    sell_ema_25_50 = ArrayField(models.FloatField(), blank=True, default=list)
    buy_ema_10_50 = ArrayField(models.FloatField(), blank=True, default=list)
    sell_ema_10_50 = ArrayField(models.FloatField(), blank=True, default=list)

    buy_sma_10_25 = ArrayField(models.FloatField(), blank=True, default=list)
    sell_sma_10_25 = ArrayField(models.FloatField(), blank=True, default=list)
    buy_sma_25_50 = ArrayField(models.FloatField(), blank=True, default=list)
    sell_sma_25_50 = ArrayField(models.FloatField(), blank=True, default=list)
    buy_sma_10_50 = ArrayField(models.FloatField(), blank=True, default=list)
    sell_sma_10_50 = ArrayField(models.FloatField(), blank=True, default=list)

    def __str__(self):
        return f"Signal {self.pk}"