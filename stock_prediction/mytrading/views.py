from django.shortcuts import render
from django.views.generic import FormView
from mytrading.forms import StocksForm
from mytrading.moving_average import MovingAverageDayTrading
import plotly.offline as plot
#from plotly.graph_objs import Scatter
import plotly.graph_objects as go
from plotly.graph_objects import Scatter
class StockFormView(FormView):

    template_name = "mytrading/home.html"
    form_class = StocksForm
    success_url = template_name

    def post(self, request):
        #breakpoint()
        form = StocksForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data.get("ticker")
            x_data = [0,1,2,3]
            y_data = [x**2 for x in x_data]
            plt_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')],
                        output_type='div')
            #plt_div = MovingAverageDayTrading(ticker, stop_loss=0.03, take_profit=0.15)
            context={"plt_div": plt_div, "ticker": ticker, "form": form}
            #if ticker:
            return render(
                    request,
                    self.template_name,
                    context
                )
        else:
            form = StocksForm()


