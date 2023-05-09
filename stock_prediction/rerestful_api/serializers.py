from rest_framework import serializers
from .models import Signal
import numpy as np
from mytrading.models import Trader

class TraderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trader
        fields = ("username","first_name", "last_name")


class SignalSerializer(serializers.ModelSerializer):
    trader = TraderSerializer()

    class Meta:
        model = Signal
        fields = (
            'trader',
            'ticker',
            'buy_emas',
            'sell_emas',
            'buy_smas',
            'sell_smas',
            'buy_ema_10_25',
            'sell_ema_10_25',
            'buy_ema_25_50',
            'sell_ema_25_50',
            'buy_ema_10_50',
            'sell_ema_10_50',
            'buy_sma_10_25',
            'sell_sma_10_25',
            'buy_sma_25_50',
            'sell_sma_25_50',
            'buy_sma_10_50',
            'sell_sma_10_50'
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for key, value in rep.items():
            if isinstance(value, list):
                rep[key] = [
                    None if (isinstance(x, float) and np.isnan(x)) else x for x in value
                ]
        return rep
