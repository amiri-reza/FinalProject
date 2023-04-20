from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from .models import Signal
from .serializers import SignalSerializer



class SignalList(generics.ListAPIView):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer
    pagination_class = PageNumberPagination


# class ReminderDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Reminder.objects.all()
#     serializer_class = ReminderSerializer


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
