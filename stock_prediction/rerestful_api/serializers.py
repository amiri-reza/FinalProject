from rest_framework import serializers
from .models import Signal
from django.contrib.auth.models import User


# class SignalSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()

#     class Meta:
#         model = Reminder
#         fields = ["id", "title", "description", "due_date", "user"]



class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = '__all__'
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for key, value in rep.items():
            if isinstance(value, list):
                rep[key] = [None if x != x else x for x in value]  # Replace NaN values with None
        return rep