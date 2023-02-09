from django.urls import path
from mytrading.views import StockFormView


urlpatterns = [
    path("", StockFormView.as_view(), name="home"),
]
