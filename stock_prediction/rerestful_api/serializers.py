from rest_framework import serializers
from .models import Signal
import numpy as np


class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for key, value in rep.items():
            if isinstance(value, list):
                rep[key] = [
                    None if (isinstance(x, float) and np.isnan(x)) else x for x in value
                ]
        return rep
