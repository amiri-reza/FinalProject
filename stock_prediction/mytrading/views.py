from django.shortcuts import render
from django.views.generic import FormView, TemplateView, UpdateView
from mytrading.forms import StocksForm
from mytrading.moving_average import MovingAverageDayTrading
import yfinance as yf
from django.contrib.auth.mixins import LoginRequiredMixin
from mytrading.models import Trader
from django.urls import reverse_lazy
from allauth.account.views import PasswordChangeView
from mytrading.locator import get_location


class StockFormView(LoginRequiredMixin, FormView):
    template_name = "mytrading/home.html"
    form_class = StocksForm
    success_url = template_name

    def post(self, request):
        form = StocksForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data.get("ticker")
            ticker_obj = yf.Ticker(ticker)
            plt_div = MovingAverageDayTrading(ticker, stop_loss=0.03, take_profit=0.15)
            context = {
                "plt_div": plt_div.moving_average_timeframes(),
                "ticker": ticker_obj,
                "form": form,
            }
            return render(request, self.template_name, context)
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
    fields = [
        "email",
        "username",
    ]
    success_url = reverse_lazy("mytrading:profile")


class CustomChangePassword(PasswordChangeView):
    def get_success_url(self) -> str:
        return reverse_lazy(
            "mytrading:update-account", kwargs={"pk": self.request.user.id}
        )


from django.shortcuts import render
from django.http import JsonResponse
from .chatbot import ChatBotSpacy
from mytrading.moving_average import MovingAverageDayTrading

def chatbot(request):

    #breakpoint()
    if request.method == 'POST':
        ticker = request.POST.get('ticker')
        statement = request.POST.get('statement')
        print("----------------------------------------", ticker, statement)
        average = MovingAverageDayTrading(ticker, df_retrieve=True, stop_loss=0.03, take_profit=0.15)
        df = average.moving_average_timeframes()

        chatbot_response = ChatBotSpacy(ticker, df, statement)
        response_text = chatbot_response.chatbot()
        print("----------------------------------------")
        if response_text is None:
            response_text = "Sorry I don't understand that. Please rephrase your statement."

        return JsonResponse({'response': response_text})

    return render(request, 'mytrading/chatbot2.html')
