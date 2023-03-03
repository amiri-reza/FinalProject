from django.shortcuts import render
from django.views.generic import FormView, DetailView, TemplateView, UpdateView
from mytrading.forms import StocksForm
from mytrading.moving_average import MovingAverageDayTrading
import yfinance as yf
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import SignupView, LoginView
from mytrading.models import Trader


class StockFormView(LoginRequiredMixin, FormView):
    template_name = "mytrading/home.html"
    form_class = StocksForm
    success_url = template_name

    def post(self, request):
        # breakpoint()
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
        # breakpoint()
        trader = request.user
        return super().get(self, request, trader=trader)


from django.shortcuts import get_object_or_404


class TraderUpdateView(UpdateView):
    # breakpoint()
    template_name = "mytrading/update-profile.html"
    model = Trader
    fields = [
        "first_name",
        "last_name",
        "email",
        "country",
        "phone_number",
        "is_subscriber",
        "interface_language",
    ]

    success_url = "/"
    # queryset = Trader.objects.all()
    # slug_field = 'trader'

    # def get_object(self, request):
    #     trader = Trader.objects.filter(username=request.user.username)
    #     return super().get_object(trader)
    # def get_object(self):
    #     breakpoint()
    #     return Trader.objects.get(pk=self.request.GET.get('pk'))

    # def get_object(self):

    #     object = get_object_or_404(Trader, username=self.kwargs.get("username"))
    #     breakpoint()
    #     # only owner can view his page
    #     if self.request.user.username == object.username:
    #         return object
    #     else:
    #         # redirect to 404 page
    #         print("you are not the owner!!")

    # def get(self, request):
    #     breakpoint()
    #     trader = request.user.username
    #     return super().get(self, request, trader=trader)


# class CustomSignupView(SignupView):
#     def form_valid(self, form):
#         #breakpoint()
#         response = super().form_valid(form)
#         self.request.session.flush() # logs the user out immediately
#         return response
