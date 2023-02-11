from django.shortcuts import render
from django.views.generic import FormView
from mytrading.forms import StocksForm
from mytrading.moving_average import MovingAverageDayTrading
import plotly.offline as plot
#from plotly.graph_objs import Scatter
import plotly.graph_objects as go
from plotly.graph_objects import Scatter
import yfinance as yf



class StockFormView(FormView):

    template_name = "mytrading/home.html"
    form_class = StocksForm
    success_url = template_name

    def post(self, request):
        #breakpoint()
        form = StocksForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data.get("ticker")
            # x_data = [0,1,2,3]
            # y_data = [x**2 for x in x_data]
            # trace1 = go.Scatter(x=x_data, y=y_data,
            #             mode='lines', name='test',
            #             opacity=0.8, marker_color='green')
            # layout = go.Layout(title="My Stocks", xaxis={'title':'x1'}, yaxis={'title':'x2'})
            # figure = go.Figure(data=trace1, layout=layout)
            
            ticker_obj = yf.Ticker(ticker)
            plt_div = MovingAverageDayTrading(ticker, stop_loss=0.03, take_profit=0.15)
            context={
                "plt_div": plt_div.moving_average_timeframes(), 
                "ticker": ticker_obj,
                "form": form
                }
            #if ticker:
            return render(
                    request,
                    self.template_name,
                    context
                )
        else:
            form = StocksForm()


