from django import forms
from django.utils import timezone
from django_countries.fields import CountryField
from mytrading.models import Trader
from mytrading.validators import age_validator
import importlib



RESTRICTION_AGE = 18


class StocksForm(forms.Form):
    ticker = forms.CharField(max_length=5)


class TradingForm(forms.Form):
    pass



SignupForm = importlib.import_module('allauth.account.forms')

class CustomSignupForm(SignupForm.SignupForm):
    date_of_birth = forms.DateField(initial=timezone.now())
    country = CountryField(default='DE').formfield()

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        age_validator(date_of_birth, RESTRICTION_AGE)
        return date_of_birth
        

    def save(self, request):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        country = self.cleaned_data.get("country")
        date_of_birth = self.clean_date_of_birth()
        
        user = Trader.objects.create_user(
            username=username,
            email=email,
            password=password,
            date_of_birth=date_of_birth,
            country=country
        )
        return user



