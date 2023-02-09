from django import forms


class StocksForm(forms.Form):
    ticker = forms.CharField(max_length=5)
