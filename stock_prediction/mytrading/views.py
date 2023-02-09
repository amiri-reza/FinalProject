from django.shortcuts import render
from django.views.generic import FormView
from mytrading.forms import StocksForm


class StockFormView(FormView):

    template_name = "mytrading/home.html"
    form_class = StocksForm
    success_url = template_name

    def post(self, request):
        breakpoint()
        form = StocksForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data.get("ticker")
            if ticker:
                return render(
                    request,
                    self.template_name,
                    context={"msg": "The Ticker will be displayed here."},
                )
        else:
            form = StocksForm()
