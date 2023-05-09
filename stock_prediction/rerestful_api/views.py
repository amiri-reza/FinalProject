from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from .models import Signal
from .serializers import SignalSerializer
from django.contrib.auth.mixins import LoginRequiredMixin


class SignalList(LoginRequiredMixin, generics.ListAPIView):
    #queryset = Signal.objects.all()
    serializer_class = SignalSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        #breakpoint()
        trader = self.request.user
        queryset = Signal.objects.filter(trader=trader)
        return queryset