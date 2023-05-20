from django.shortcuts import render
from django.views.generic import FormView, TemplateView, UpdateView
from mytrading.forms import StocksForm, UpdateAccountForm
from mytrading.moving_average import MovingAverageDayTrading
import yfinance as yf
from django.contrib.auth.mixins import LoginRequiredMixin
from mytrading.models import Trader
from django.urls import reverse_lazy
from allauth.account.views import PasswordChangeView
from mytrading.locator import get_location
from django.http import JsonResponse
from .chatbot import ChatBotSpacy
from django.contrib import messages
import os


class StockFormView(LoginRequiredMixin, FormView):
    template_name = "mytrading/home.html"
    form_class = StocksForm
    success_url = template_name

    def read_ticker_file(self, request):
        ticker = request.POST.get("ticker")
        curr = os.getcwd()
        file_path = os.path.join(curr, "static", "txt", "NASDAQ.txt")
        with open(file_path, "r") as file:
            lines = file.readlines()
        ticker_list = [tuple(line.strip().split("\t")) for line in lines]
        for symbol, company in ticker_list:
            if symbol == ticker.upper():
                return company

    def post(self, request):
        form = StocksForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data.get("ticker")
            ticker_obj = yf.Ticker(ticker)
            user = request.user
            plt_div = MovingAverageDayTrading(ticker, user, stop_loss=0.03, take_profit=0.15)
            context = {
                "plt_div": plt_div.moving_average_timeframes(),
                "ticker": ticker_obj,
                "form": form,
                "company": self.read_ticker_file(request),
            }
            return render(request, "mytrading/home.html", context)
        else:
            form = StocksForm()


class TraderProfileView(TemplateView):
    model = Trader
    template_name = "mytrading/profile.html"

    def get(self, request):
        trader = request.user
        trader.login_location = get_location(request)

        return super().get(self, request, trader=trader)


class TraderUpdateView(UpdateView):
    template_name = "mytrading/update-profile.html"
    model = Trader
    fields = [
        "first_name",
        "last_name",
        "country",
        "phone_number",
        "is_subscriber",
        "interface_language",
    ]
    success_url = reverse_lazy("mytrading:profile")


class SecuritySettingsView(UpdateView):
    template_name = "mytrading/update-account.html"
    model = Trader
    form_class = UpdateAccountForm
    success_url = reverse_lazy("mytrading:profile")

    def form_invalid(self, form):
        username_errors = form.errors.get("username")
        if username_errors:
            messages.error(self.request, username_errors[0])
        email_errors = form.errors.get("email")
        if email_errors:
            messages.error(self.request, email_errors[0])
        return super().form_invalid(form)


class CustomChangePassword(PasswordChangeView):
    def get_success_url(self) -> str:
        return reverse_lazy(
            "mytrading:update-account", kwargs={"pk": self.request.user.id}
        )


def chatbot(request):
    if request.method == "POST":
        ticker = request.POST.get("ticker")
        statement = request.POST.get("statement")
        average = MovingAverageDayTrading(
            ticker, df_retrieve=True, stop_loss=0.03, take_profit=0.15
        )
        df = average.moving_average_timeframes()

        chatbot_response = ChatBotSpacy(ticker, df, statement)
        response_text = chatbot_response.chatbot()
        if response_text is None:
            response_text = (
                "Sorry I don't understand that. Please rephrase your statement."
            )
        return JsonResponse({"response": response_text})

    return render(request, "mytrading/chatbot2.html")
