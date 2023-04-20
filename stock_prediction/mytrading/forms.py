from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django_countries.fields import CountryField
from mytrading.models import Trader
from mytrading.validator import age_validator
import importlib
from allauth.account.adapter import get_adapter
from django.conf import settings
from mytrading.locator import get_location
SignupForm = importlib.import_module("allauth.account.forms")

class StocksForm(forms.Form):
    ticker = forms.CharField(max_length=5)



class CustomSignupForm(SignupForm.SignupForm):
    date_of_birth = forms.DateField(initial=timezone.now())
    country = CountryField(default="DE").formfield()

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get("date_of_birth")
        age_validator(date_of_birth, settings.RESTRICTION_AGE)
        return date_of_birth

    def clean(self):
        super(CustomSignupForm, self).clean()
        password = self.cleaned_data.get("password1")
        if password:
            try:
                get_adapter().clean_password(password, user=None)
            except forms.ValidationError as e:
                self.add_error("password1", e)
        return self.cleaned_data

    def save(self, request):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password1")
        country = self.cleaned_data.get("country")
        date_of_birth = self.clean_date_of_birth()
        login_location = get_location(request)

        user = Trader.objects.create_user(
            username=username,
            email=email,
            password=password,
            date_of_birth=date_of_birth,
            country=country,
            login_location=login_location,
        )
        return user




class UpdateAccountForm(forms.ModelForm):
    class Meta:
        model = Trader
        fields = [
            "email",
            "username",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if Trader.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            print(username, '---------------------------------' )
            raise forms.ValidationError("Username is already taken.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Trader.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("Email is already in use.")
        return email