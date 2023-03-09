from django.urls import path
from mytrading.views import (
    StockFormView,
    TraderProfileView,
    TraderUpdateView,
    SecuritySettingsView,
    CustomChangePassword,
)

app_name = "mytrading"
urlpatterns = [
    path("", StockFormView.as_view(), name="home"),
    path("profile/", TraderProfileView.as_view(), name="profile"),
    path("trader/edit/<int:pk>/", TraderUpdateView.as_view(), name="update-profile"),
    path(
        "trader/settings/<int:pk>/",
        SecuritySettingsView.as_view(),
        name="update-account",
    ),
    path(
        "trader/settings/password/",
        CustomChangePassword.as_view(),
        name="change-password",
    ),
]
