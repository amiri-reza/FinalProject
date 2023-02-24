from django import forms
import importlib
# from allauth.account.forms import BaseSignupForm
from datetime import date
from mytrading.models import Trader



class StocksForm(forms.Form):
    ticker = forms.CharField(max_length=5)


class TradingForm(forms.Form):
    pass



SignupForm = importlib.import_module('allauth.account.forms')

class CustomSignupForm(SignupForm.SignupForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1920, 2023)))
    def save(self, request):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        date_of_birth = self.cleaned_data.get("date_of_birth")
        
        user = Trader.objects.create_user(
            username=username,
            email=email,
            password=password,
            date_of_birth=date_of_birth
        )
        return user



