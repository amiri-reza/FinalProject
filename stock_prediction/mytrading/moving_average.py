import dash
from dash import dcc
from dash import html
import plotly.express as xp
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import timedelta, datetime
import time
import talib as ta
import pytz



class MovingAverageDayTrading():

    def __init__(self, ticker, stop_loss=0.05, take_profit=0.1):
        self.ticker = ticker
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        # This way, when an instance of the class is created, the self.stop_loss and self.take_profit will be set with default values of 0.05 and 0.1 respectively. These values can be overridden when an instance of the class is created by passing a different value for stop_loss and take_profit.

    def moving_average_timeframes(self):
        
        #  QUERYING DATA --------------------------------------------
        while True:
            end= datetime.today()
            start = end - timedelta(days=7)
            df = yf.download(self.ticker, start= start ,end= end, interval='1m')
            print(f'--------{df}__________')
            print(df.dtypes)
            print(f'index typeeeee : {df.index.dtype}')
            
            # check the interval of your dataframe by using the df.resample function with the same interval of data you want to work with
            ## df.resample('1min')

            #  SETTING UP DATA: ADDING COLUMNS FOR MA  --------------------------------------

            # Exponential Moving Averages
            df['EMA_10'] = df['Adj Close'].ewm(span=10, adjust=False).mean()
            df['EMA_25'] = df['Adj Close'].ewm(span=25, adjust=False).mean()
            df['EMA_50'] = df['Adj Close'].ewm(span=50, adjust=False).mean()
            # the ewm() method to calculate the EMA, passing in the window size or span, which is the number of periods to use in the moving average. You can also adjust whether or not to apply some decay to the weights by adjusting the adjust parameter. By default is set to True, but it depends on the use case.

            # Simple Moving Averages
            df['SMA_5'] = df['Close'].rolling(window=5).mean()
            df['SMA_8'] = df['Close'].rolling(window=8).mean()
            df['SMA_13'] = df['Close'].rolling(window=13).mean()

            # Bollinger Bands
            df['BOL_upper'], df['BOL_middle'], df['BOL_lower'] = ta.BBANDS(df["Adj Close"])
            
            # Stochastic Oscillator
            df['STO_slowk'], df['STO_slowd'] = ta.STOCH(df["High"], df["Low"], df["Adj Close"])
            
            # Relative Strength Index
            df['RSI'] = ta.RSI(df["Adj Close"])
            
            # Moving Average Convergence Divergence
            df['MACD'], df['MACD_signal'], df['MACD_hist'] = ta.MACD(df["Adj Close"])
            
            
            # CLEANING DATA ------------------------------------------

            print(df.dtypes)

            # check if the data is sorted correctly by running 
            df.sort_index(inplace=True)

            # fill the empty spaces with what we want to fill it out
            df.fillna(method='ffill', inplace=True)


            print(f'HHHHHHHHHHHHHH {type(df.index)}')
            
            # Remove any rows with missing values
            df = df.dropna()
            
            # df = df[['Adj Close', 'EMA_10', 'EMA_25', 'EMA_50', 'SMA_5', 'SMA_8', 'SMA_13', 'BOL_upper','STO_slowk', 'RSI', 'MACD']]

            print(f'SHAPEEEEEEEEEEE  {df.shape}')

            
            if self.stop_loss is None or self.take_profit is None:
                raise ValueError("stop_loss and take_profit values must be set before using them")

            #  LOGIC BUY AND SELLS SIGNALS  ----------------------------

            signals = {}
            


            # DEBUGGING --------
            
            print(df)
            print(f'@@@@@@@@@@{df.columns}@@@@@@@@@@')
            print(df.columns[0])
            
            print(f'fFFFFFFFFFFFFFFFF {df.index}')
            print(df['EMA_10'])
            
            # FINDING THE GAPS IN THE INDEX OR X AXE TO REFRAME THE DATAFRAME TO ERASE THE SPACES FROM DATA WE PREV CLEANED -----------

            # Specify minimum time gap in nanoseconds. 
            TIME_GAP = 60000000000

            # get an index array where there is a time gap
            gap_idx = np.where(np.diff(df.index.astype(int)) > TIME_GAP)[0]

            df = df.reset_index()

            # use numpy to insert nans
            df = pd.DataFrame(
                columns = df.columns, 
                data = np.insert(df.values, gap_idx+1, values=np.nan, axis=0)
                )

            df = df.set_index('Datetime')

            # PLOTTING WITH MATPLOTLIB ----------------------------------------------
            
            # fig = go.Figure()
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.03, subplot_titles=(f'{self.ticker}', '', 'Volume'), row_width=[0.2, 0.7])
            fig.add_trace(go.Scatter(x=df.index, y=df['Adj Close'], mode='lines', name='Asset price',line=dict(width=2)))
            fig.add_trace(go.Scatter(x=df.index, y=df['EMA_10'], mode='lines', name='EMA_10'))
            fig.add_trace(go.Scatter(x=df.index, y=df['EMA_25'], mode='lines', name='EMA_25'))
            fig.add_trace(go.Scatter(x=df.index, y=df['EMA_50'], mode='lines', name='EMA_50'))
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_5'], mode='lines', name='SMA_5'))
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_8'], mode='lines', name='SMA_8'))
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_13'], mode='lines', name='SMA_13'))
            fig.add_trace(go.Scatter(x=df.index, y=df['BOL_upper'], mode='lines', name='BOL_upper'))
            fig.add_trace(go.Scatter(x=df.index, y=df['BOL_middle'], mode='lines', name='BOL_middle'))
            fig.add_trace(go.Scatter(x=df.index, y=df['BOL_lower'], mode='lines', name='BOL_lower'))
            fig.add_trace(go.Scatter(x=df.index, y=df['STO_slowk'], mode='lines', name='STO_slowk'))
            fig.add_trace(go.Scatter(x=df.index, y=df['STO_slowd'], mode='lines', name='STO_slowd'))
            fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI'))
            fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], mode='lines', name='MACD'))
            fig.add_trace(go.Scatter(x=df.index, y=df['MACD_signal'], mode='lines', name='MACD_signal'))
            # include candlestick with rangeselector
            fig.add_trace(go.Candlestick(x=df.index,
                            open=df['Open'], high=df['High'],
                            low=df['Low'], close=df['Close']),
                            row=1,
                            col=1
                            )

        
            fig.update_xaxes(
                row=1,
                col=1,
                rangeslider_visible=False,
                rangeselector=dict(
                    buttons=[
                        dict(count=1, label="1m", step="minute", stepmode="todate"),
                        dict(count=1, label="1h", step="hour", stepmode="todate"),
                        dict(count=1, label="1d", step="day", stepmode="todate"),
                        dict(step="all")
                        ]),
                    rangebreaks=[
                        dict(bounds=[16, 9.5], pattern="hour"), #hide hours outside of 9.30am-4pm
                        dict(bounds=["sat", "mon"]), #hide weekends
                        dict(values=["2015-12-25", "2016-01-01"])  # hide Christmas and New Year's
                        ]
            )


            # Bar trace for volumes on 2nd row without legend
            fig.add_trace(go.Bar(x=df.index, y=df['Volume'], showlegend=False, marker=dict(color='lightcoral', opacity=1, line=dict(width=2, color="lightcoral"))), row=2, col=1)
            # Do not show others's rangeslider plot 
            fig.update(layout_xaxis_rangeslider_visible=False)

            fig.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        buttons=[
                            dict(
                                label="Candlestick",
                                method="update",
                                args=[
                                    {"visible": [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True ]},
                                    {"title": "Candlestick"}
                                ]
                            ),
                            dict(
                                label="Candlestick & EMAs",
                                method="update",
                                args=[
                                    {"visible": [True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, True, True ]},
                                    {"title": "Candlestick & EMAs"}
                                ]
                            ),
                            dict(
                                label="Candlestick & SMAs",
                                method="update",
                                args=[
                                    {"visible": [True, False, False, False, True, True, True, False, False, False, False, False, False, False, False, True, True ]},
                                    {"title": "Candlestick & SMAs"}
                                ]
                            ),
                            dict(
                                label="EMAs",
                                method="update",
                                args=[
                                    {"visible": [True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, True ]},
                                    {"title": "Asset price & EMAs"}
                                ]
                            ),
                            dict(
                                label="SMAs",
                                method="update",
                                args=[
                                    {"visible": [True, False, False, False, True, True, True, False, False, False, False, False, False, False, False, False, True ]},
                                    {"title": "SMAs"}
                                ]
                            ),
                            dict(
                                label="EMA_10 & EMA_25",
                                method="update",
                                args=[
                                    {"visible": [True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, True ]},
                                    {"title": "EMA_10 & EMA_25"}
                                ]
                            ),
                            dict(
                                label="EMA_10 and EMA_50",
                                method="update",
                                args=[
                                    {"visible": [True, True, False, True, False, False, False, False, False, False, False, False, False, False, False, False, True ]},
                                    {"title": "EMA_10 and EMA_50"}
                                ]
                            ),
                            dict(
                                label="EMA_25 and EMA_50",
                                method="update",
                                args=[
                                    {"visible": [True, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, True ]},
                                    {"title": "EMA_25 and EMA_50"}
                                ]
                            ),
                            dict(
                                label="SMA_5 and SMA_8",
                                method="update",
                                args=[
                                    {"visible": [True, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, True ]},
                                    {"title": "SMA_5 and SMA_8"}
                                ]
                            ),
                            dict(
                                label="SMA_5 and SMA_13",
                                method="update",
                                args=[
                                    {"visible": [True, False, False, False, True, False, True, False, False, False, False, False, False, False, False, False, True ]},
                                    {"title": "SMA_5 and SMA_13"}
                                ]
                            ),
                            dict(
                                label="SMA_8 and SMA_13",
                                method="update",
                                args=[
                                    {"visible": [True, False, False, False, False, True, True, False, False, False, False, False, False, False, False, False, True ]},
                                    {"title": "SMA_8 and SMA_13"}
                                ]
                            ),
                            dict(
                                label="BOL_upper & BOL_middle & BOL_lower",
                                method="update",
                                args=[
                                    {"visible": [True, False, False, False, False, False, False, True, True, True, False, False, False, False, False, False, True ]},
                                    {"title": "BOL_upper & BOL_middle & BOL_lower"}
                                ]
                            ),
                            dict(
                                label="STO_slowk & STO_slowd",
                                method="update",
                                args=[
                                    {"visible": [True, False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, True ]},
                                    {"title": "STO_slowk & STO_slowd"}
                                ]
                            ),
                            dict(
                                label="RSI",
                                method="update",
                                args=[
                                    {"visible": [True, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, True ]},
                                    {"title": "RSI"}
                                ]
                            ),
                            dict(
                                label="MACD & MACD_signal",
                                method="update",
                                args=[
                                    {"visible": [True, False, False, False, False, False, False, False, False, False, False, False, False, True, True, False, True ]},
                                    {"title": "MACD"}
                                ]
                            ),
                            dict(
                                label="All",
                                method="update",
                                args=[
                                    {"visible": [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True ]},
                                    {"title": "All"}
                                ]
                            ),
                        ]
                    )
                ]
            )


        
            time.sleep(3600/2000)
            return fig.show()


if __name__ == '__main__':
    
    average = MovingAverageDayTrading('GOOG', stop_loss=0.03, take_profit=0.15)
    average.moving_average_timeframes()