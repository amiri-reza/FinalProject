from django.urls import path
from mytrading.views import StockFormView, TraderProfileView, TraderUpdateView

app_name = "mytrading"
urlpatterns = [
    path("", StockFormView.as_view(), name="home"),
    path("profile/", TraderProfileView.as_view(), name="profile"),
    path("trader/edit/<int:pk>", TraderUpdateView.as_view(), name="update-profile"),
]
