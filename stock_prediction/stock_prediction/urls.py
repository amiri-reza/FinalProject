"""stock_prediction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from stock_prediction.views import Home
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib import admin
from rerestful_api.views import SignalList

urlpatterns = [
    path(
        "favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("img/icon.ico"))
    ),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("home/", include("mytrading.urls")),
    path("", Home.as_view(), name="landing_page"),
    path("restful_api/", SignalList.as_view(), name="signal-list"),
    

]