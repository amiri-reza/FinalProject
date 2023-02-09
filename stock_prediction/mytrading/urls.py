
from django.urls import path
from mytrading.views import FormView
from django.views.generic import TemplateView


urlpatterns = [
    path("", FormView.as_view(), name="trading"),
    path("test", TemplateView.as_view(template_name="mytrading/trading.html"))
    
]











