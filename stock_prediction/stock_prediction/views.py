from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import forms


class Home(TemplateView):
    template_name = "account/login.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")

        return super().dispatch(request, *args, **kwargs)
