from django.views.generic import TemplateView
from django.shortcuts import redirect


class Home(TemplateView):
    template_name = "home.html"

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return redirect("account_login")
    #     if request.user.is_authenticated:
    #         return redirect("home/")

    #     return super().dispatch(request, *args, **kwargs)
