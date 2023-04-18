import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as plot
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import timedelta, datetime
import time
import talib as ta
import time
from django.core.mail import send_mail


class MovingAverageDayTrading:
    def __init__(self, ticker, df_retrieve=False, stop_loss=0.05, take_profit=0.1):
        self.ticker = ticker
        self.df_retrieve = df_retrieve
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        # This way, when an instance of the class is created, the self.stop_loss and self.take_profit will be set with default values of 0.05 and 0.1 respectively. These values can be overridden when an instance of the class is created by passing a different value for stop_loss and take_profit.

    def moving_average_timeframes(self):
        #  QUERYING DATA --------------------------------------------
        while True:
            end = datetime.today()
            start = end - timedelta(days=7)
            df = yf.download(self.ticker, start=start, end=end, interval="1m")
            print(f"--------{df}__________")
            print(df.dtypes)
            print(f"index typeeeee : {df.index.dtype}")

            # check the interval of your dataframe by using the df.resample function with the same interval of data you want to work with
            ## df.resample('1min')

            #  SETTING UP DATA: ADDING COLUMNS FOR MA  --------------------------------------

            # TECHNICAL INDICATORS
            # Exponential Moving Averages
            df["EMA_10"] = df["Adj Close"].ewm(span=10, adjust=False).mean()
            df["EMA_25"] = df["Adj Close"].ewm(span=25, adjust=False).mean()
            df["EMA_50"] = df["Adj Close"].ewm(span=50, adjust=False).mean()
            # the ewm() method to calculate the EMA, passing in the window size or span, which is the number of periods to use in the moving average. You can also adjust whether or not to apply some decay to the weights by adjusting the adjust parameter. By default is set to True, but it depends on the use case.

            # Simple Moving Averages
            df["SMA_10"] = df["Close"].rolling(window=10).mean()
            df["SMA_25"] = df["Close"].rolling(window=25).mean()
            df["SMA_50"] = df["Close"].rolling(window=50).mean()

            # Bollinger Bands
            df["BOL_upper"], df["BOL_middle"], df["BOL_lower"] = ta.BBANDS(
                df["Adj Close"]
            )

            # Stochastic Oscillator
            df["STO_slowk"], df["STO_slowd"] = ta.STOCH(
                df["High"], df["Low"], df["Adj Close"]
            )

            # Relative Strength Index
            df["RSI"] = ta.RSI(df["Adj Close"])

            # Moving Average Convergence Divergence
            df["MACD"], df["MACD_signal"], df["MACD_hist"] = ta.MACD(df["Adj Close"])

            # CLEANING DATA ------------------------------------------

            print(df.dtypes)

            # check if the data is sorted correctly by running
            df.sort_index(inplace=True)

            # fill the empty spaces with what we want to fill it out
            df.fillna(method="ffill", inplace=True)

            print(f"HHHHHHHHHHHHHH {type(df.index)}")

            # Remove any rows with missing values
            df = df.dropna()

            # df = df[['Adj Close', 'EMA_10', 'EMA_25', 'EMA_50', 'SMA_5', 'SMA_8', 'SMA_13', 'BOL_upper','STO_slowk', 'RSI', 'MACD']]

            print(f"SHAPEEEEEEEEEEE  {df.shape}")

            if self.stop_loss is None or self.take_profit is None:
                raise ValueError(
                    "stop_loss and take_profit values must be set before using them"
                )

            # DEBUGGING --------

            print(df)
            print(f"@@@@@@@@@@{df.columns}@@@@@@@@@@")
            print(df.columns[0])

            print(f"fFFFFFFFFFFFFFFFF {df.index}")
            print(df["EMA_10"])

            # FINDING THE GAPS IN THE INDEX OR X AXE TO REFRAME THE DATAFRAME TO ERASE THE SPACES FROM DATA WE PREV CLEANED -----------

            # Specify minimum time gap in nanoseconds.
            TIME_GAP = 60000000000

            # get an index array where there is a time gap
            gap_idx = np.where(np.diff(df.index.astype(int)) > TIME_GAP)[0]

            df = df.reset_index()

            # use numpy to insert nans
            df = pd.DataFrame(
                columns=df.columns,
                data=np.insert(df.values, gap_idx + 1, values=np.nan, axis=0),
            )

            df = df.set_index("Datetime")

            #  LOGIC BUY AND SELLS SIGNALS  ----------------------------

            # # Create empty lists to store buy and sell signals
            buy_emas = []
            sell_emas = []
            buy_smas = []
            sell_smas = []

            def signals(ma_1, ma_2, ma_3, df, list1, list2, buy, sell):
                mask1 = (
                    (df[ma_1] > df["Adj Close"])
                    & (df[ma_2] > df["Adj Close"])
                    & (df[ma_3] > df["Adj Close"])
                )
                mask2 = (
                    (df[ma_1] < df["Adj Close"])
                    & (df["EMA_25"] < df["Adj Close"])
                    & (df["EMA_50"] < df["Adj Close"])
                )

                df[buy] = df["Adj Close"]
                df[sell] = df["Adj Close"]

                df.loc[mask1, sell] = np.nan
                df.loc[mask2, buy] = np.nan

                df[buy] = df[buy].where(
                    df.groupby(mask2.cumsum()).cumcount() <= 1, np.nan
                )
                df[sell] = df[sell].where(
                    df.groupby(mask1.cumsum()).cumcount() <= 1, np.nan
                )

            # def signals(ma_1, ma_2, ma_3, df, list1, list2, buy, sell):

            #     for date, row in df.iterrows():
            #         if (
            #             (row[ma_1] < row["Adj Close"])
            #             & (row[ma_2] < row["Adj Close"])
            #             & (row[ma_3] < row["Adj Close"])
            #         ):
            #             list1.append(date)

            #         if (
            #             (row[ma_1] > row["Adj Close"])
            #             & (row["EMA_25"] > row["Adj Close"])
            #             & (row["EMA_50"] > row["Adj Close"])
            #         ):
            #             list2.append(date)

            #     df[buy] = df["Adj Close"]
            #     df[sell] = df["Adj Close"]
            #     for date in df.index:
            #         if date not in list1:
            #             df[buy].at[date] = np.nan
            #         if date not in list2:
            #             df[sell].at[date] = np.nan

            signals(
                "EMA_10",
                "EMA_25",
                "EMA_50",
                df,
                buy_emas,
                sell_emas,
                "BUY_EMAs",
                "SELL_EMAs",
            )
            signals(
                "SMA_10",
                "SMA_25",
                "SMA_50",
                df,
                buy_smas,
                sell_smas,
                "BUY_SMAs",
                "SELL_SMAs",
            )

            # single cross
            buy_ema_10_25 = []
            sell_ema_10_25 = []
            buy_ema_25_50 = []
            sell_ema_25_50 = []
            buy_ema_10_50 = []
            sell_ema_10_50 = []

            buy_sma_10_25 = []
            sell_sma_10_25 = []
            buy_sma_25_50 = []
            sell_sma_25_50 = []
            buy_sma_10_50 = []
            sell_sma_10_50 = []

            def signal_cross(ma_1, ma_2, df, list1, list2, buy, sell):
                mask1 = df[ma_1] > df[ma_2]
                mask2 = df[ma_1] < df[ma_2]

                df[buy] = df["Adj Close"]
                df[sell] = df["Adj Close"]

                df.loc[mask1, sell] = np.nan
                df.loc[mask2, buy] = np.nan

                df[buy] = df[buy].where(
                    df.groupby(mask2.cumsum()).cumcount() <= 1, np.nan
                )
                df[sell] = df[sell].where(
                    df.groupby(mask1.cumsum()).cumcount() <= 1, np.nan
                )

            # def signal_cross(ma_1, ma_2, df, list1, list2, buy, sell):

            #     for date, row in df.iterrows():
            #         if row[ma_1] < row[ma_2]:
            #             list2.append(date)

            #         if row[ma_1] > row[ma_2]:
            #             list1.append(date)

            #     df[buy] = df["Adj Close"]
            #     df[sell] = df["Adj Close"]
            #     for date in df.index:
            #         if date not in list1:
            #             df[buy].at[date] = np.nan
            #         if date not in list2:
            #             df[sell].at[date] = np.nan

            signal_cross(
                "EMA_10",
                "EMA_25",
                df,
                buy_ema_10_25,
                sell_ema_10_25,
                "BUY_EMA_10_25",
                "SELL_EMA_10_25",
            )
            signal_cross(
                "EMA_25",
                "EMA_50",
                df,
                buy_ema_25_50,
                sell_ema_25_50,
                "BUY_EMA_25_50",
                "SELL_EMA_25_50",
            )
            signal_cross(
                "EMA_10",
                "EMA_50",
                df,
                buy_ema_10_50,
                sell_ema_10_50,
                "BUY_EMA_10_50",
                "SELL_EMA_10_50",
            )

            signal_cross(
                "SMA_10",
                "SMA_25",
                df,
                buy_sma_10_25,
                sell_sma_10_25,
                "BUY_SMA_10_25",
                "SELL_SMA_10_25",
            )
            signal_cross(
                "SMA_25",
                "SMA_50",
                df,
                buy_sma_25_50,
                sell_sma_25_50,
                "BUY_SMA_25_50",
                "SELL_SMA_25_50",
            )
            signal_cross(
                "SMA_10",
                "SMA_50",
                df,
                buy_sma_10_50,
                sell_sma_10_50,
                "BUY_SMA_10_50",
                "SELL_SMA_10_50",
            )

            buy_bollinger = []
            sell_bollinger = []

            def bollinger_bands(
                bol_lower, bol_middle, bol_upper, df, list1, list2, buy, sell
            ):
                for date, row in df.iterrows():
                    if (row[bol_middle] < row[bol_upper]) and (
                        row[bol_middle] > row[bol_lower]
                    ):
                        # Asset price remaining within Bollinger Bands
                        pass
                    elif (row[bol_middle] >= row[bol_upper]) and (
                        row[bol_middle] > row[bol_lower]
                    ):
                        # Asset price crossing above upper Bollinger Band or touching the upper Bollinger Band and then crossing back down
                        list2.append(date)
                    elif (row[bol_middle] <= row[bol_lower]) and (
                        row[bol_middle] < row[bol_upper]
                    ):
                        # Asset price crossing below lower Bollinger Band or touching the lower Bollinger Band and then crossing back up
                        list1.append(date)
                    elif row[bol_middle] > row[bol_upper]:
                        # Asset price exiting Bollinger Bands
                        list2.append(date)
                    elif row[bol_middle] < row[bol_lower]:
                        # Asset price approaching lower Bollinger Band
                        list1.append(date)

                df[buy] = df["Adj Close"]
                df[sell] = df["Adj Close"]
                for date in df.index:
                    if date not in list1:
                        df[buy].at[date] = np.nan
                    if date not in list2:
                        df[sell].at[date] = np.nan

            bollinger_bands(
                "BOL_lower",
                "BOL_middle",
                "BOL_upper",
                df,
                buy_bollinger,
                sell_bollinger,
                "BUY_bollinger",
                "SELL_bollinger",
            )
            print(buy_bollinger)
            print(sell_bollinger)

            # buy_sma_10_50 = []
            # sell_sma_10_50 = []

            # def stochastic_oscillator(
            #     sto_slowk, sto_slowd, df, list1, list2, buy, sell
            # ):

            #     for date, row in df.iterrows():
            #         # for loop with the logic to find buy and sell signals
            #         for date, row in df.iterrows():
            #             if row[sto_slowk] > row[sto_slowd] and row[sto_slowk].shift(
            #                 1
            #             ) <= row[sto_slowd].shift(1):
            #                 list1.append(date)
            #             if row[sto_slowk] < row[sto_slowd] and row[sto_slowk].shift(
            #                 1
            #             ) >= row[sto_slowd].shift(1):
            #                 list2.append(date)

            #     df[buy] = df["Adj Close"]
            #     df[sell] = df["Adj Close"]
            #     for date in df.index:
            #         if date not in list1:
            #             df[buy].at[date] = np.nan
            #         if date not in list2:
            #             df[sell].at[date] = np.nan

            # stochastic_oscillator(
            #     "EMA_10",
            #     "EMA_25",
            #     df,
            #     buy_ema_10_25,
            #     sell_ema_10_25,
            #     "BUY_EMA_10_25",
            #     "SELL_EMA_10_25",
            # )
            print(df)
            if self.df_retrieve:
                return df
            # PLOTTING WITH PLOTLY ----------------------------------------------

            # fig = go.Figure()
            fig = make_subplots(
                rows=2,
                cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                subplot_titles=(f"{self.ticker}", "", "Volume"),
                row_width=[0.2, 0.7],
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["Adj Close"],
                    mode="lines",
                    name="Asset price",
                    line=dict(width=2),
                )
            )

            fig.add_trace(
                go.Scatter(x=df.index, y=df["EMA_10"], mode="lines", name="EMA_10")
            )
            fig.add_trace(
                go.Scatter(x=df.index, y=df["EMA_25"], mode="lines", name="EMA_25")
            )
            fig.add_trace(
                go.Scatter(x=df.index, y=df["EMA_50"], mode="lines", name="EMA_50")
            )
            fig.add_trace(
                go.Scatter(x=df.index, y=df["SMA_10"], mode="lines", name="SMA_10")
            )
            fig.add_trace(
                go.Scatter(x=df.index, y=df["SMA_25"], mode="lines", name="SMA_25")
            )
            fig.add_trace(
                go.Scatter(x=df.index, y=df["SMA_50"], mode="lines", name="SMA_50")
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index, y=df["BOL_upper"], mode="lines", name="BOL_upper"
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index, y=df["BOL_middle"], mode="lines", name="BOL_middle"
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index, y=df["BOL_lower"], mode="lines", name="BOL_lower"
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index, y=df["STO_slowk"], mode="lines", name="STO_slowk"
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index, y=df["STO_slowd"], mode="lines", name="STO_slowd"
                )
            )
            fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], mode="lines", name="RSI"))
            fig.add_trace(
                go.Scatter(x=df.index, y=df["MACD"], mode="lines", name="MACD")
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index, y=df["MACD_signal"], mode="lines", name="MACD_signal"
                )
            )
            # include candlestick with rangeselector
            fig.add_trace(
                go.Candlestick(
                    x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                ),
                row=1,
                col=1,
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
                        dict(step="all"),
                    ]
                ),
                rangebreaks=[
                    dict(
                        bounds=[16, 9.5], pattern="hour"
                    ),  # hide hours outside of 9.30am-4pm
                    dict(bounds=["sat", "mon"]),  # hide weekends
                    dict(
                        values=["2015-12-25", "2016-01-01"]
                    ),  # hide Christmas and New Year's
                ],
            )

            # Bar trace for volumes on 2nd row without legend
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df["Volume"],
                    showlegend=False,
                    marker=dict(
                        color="lightcoral",
                        opacity=1,
                        line=dict(width=2, color="lightcoral"),
                    ),
                ),
                row=2,
                col=1,
            )
            # Do not show others's rangeslider plot
            fig.update(layout_xaxis_rangeslider_visible=False)

            # Plot the BUY and SELL signals here
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["BUY_EMAs"],
                    mode="markers",
                    name="Buy signals",
                    marker=dict(color="green"),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["SELL_EMAs"],
                    mode="markers",
                    name="Sell signals",
                    marker=dict(color="red"),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["BUY_EMAs"],
                    mode="markers",
                    name="Buy signals",
                    marker=dict(color="green"),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["SELL_EMAs"],
                    mode="markers",
                    name="Sell signals",
                    marker=dict(color="red"),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["BUY_EMA_10_25"],
                    mode="markers",
                    name="Buy signals",
                    marker=dict(color="green"),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["SELL_EMA_10_25"],
                    mode="markers",
                    name="Sell signals",
                    marker=dict(color="red"),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["BUY_EMA_25_50"],
                    mode="markers",
                    name="Buy signals",
                    marker=dict(color="green"),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["SELL_EMA_25_50"],
                    mode="markers",
                    name="Sell signals",
                    marker=dict(color="red"),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["BUY_EMA_10_50"],
                    mode="markers",
                    name="Buy signals",
                    marker=dict(color="green"),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["SELL_EMA_10_50"],
                    mode="markers",
                    name="Sell signals",
                    marker=dict(color="red"),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["BUY_SMA_10_25"],
                    mode="markers",
                    name="Buy signals",
                    marker=dict(color="green"),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["SELL_SMA_10_25"],
                    mode="markers",
                    name="Sell signals",
                    marker=dict(color="red"),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["BUY_SMA_25_50"],
                    mode="markers",
                    name="Buy signals",
                    marker=dict(color="green"),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["SELL_SMA_25_50"],
                    mode="markers",
                    name="Sell signals",
                    marker=dict(color="red"),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["BUY_bollinger"],
                    mode="markers",
                    name="Buy signals",
                    marker=dict(color="green"),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["SELL_bollinger"],
                    mode="markers",
                    name="Sell signals",
                    marker=dict(color="red"),
                )
            )

            fig.update_layout(
                updatemenus=[
                    dict(
                        type="dropdown",
                        buttons=[
                            dict(
                                label="Candlestick",
                                method="update",
                                args=[
                                    {
                                        "visible": [
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                        ]
                                    },
                                    {"title": "Candlestick"},
                                ],
                            ),
                            dict(
                                label="Candlestick & EMAs",
                                method="update",
                                args=[
                                    {
                                        "visible": [
                                            True,
                                            True,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                        ]
                                    },
                                    {"title": "Candlestick & EMAs"},
                                ],
                            ),
                            dict(
                                label="Candlestick & SMAs",
                                method="update",
                                args=[
                                    {
                                        "visible": [
                                            True,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                        ]
                                    },
                                    {"title": "Candlestick & SMAs"},
                                ],
                            ),
                            dict(
                                label="EMAs",
                                method="update",
                                args=[
                                    {
                                        "visible": [
                                            True,
                                            True,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                        ]
                                    },
                                    {"title": "Asset price & EMAs"},
                                ],
                            ),
                            dict(
                                label="SMAs",
                                method="update",
                                args=[
                                    {
                                        "visible": [
                                            True,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            False,
                                            False,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                        ]
                                    },
                                    {"title": "SMAs"},
                                ],
                            ),
                            dict(
                                label="EMA_10 & EMA_25",
                                method="update",
                                args=[
                                    {
                                        "visible": [
                                            True,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                        ]
                                    },
                                    {"title": "EMA_10 & EMA_25"},
                                ],
                            ),
                            dict(
                                label="EMA_10 and EMA_50",
                                method="update",
                                args=[
                                    {
                                        "visible": [
                                            True,
                                            True,
                                            False,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                        ]
                                    },
                                    {"title": "EMA_10 and EMA_50"},
                                ],
                            ),
                            dict(
                                label="EMA_25 and EMA_50",
                                method="update",
                                args=[
                                    {
                                        "visible": [
                                            True,
                                            False,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                        ]
                                    },
                                    {"title": "EMA_25 and EMA_50"},
                                ],
                            ),
                            dict(
                                label="SMA_10 and SMA_25",
                                method="update",
                                args=[
                                    {
                                        "visible": [
                                            True,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                        ]
                                    },
                                    {"title": "SMA_10 and SMA_25"},
                                ],
                            ),
                            dict(
                                label="SMA_10 and SMA_50",
                                method="update",
                                args=[
                                    {
                                        "visible": [
                                            True,
                                            False,
                                            False,
                                            False,
                                            True,
                                            False,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            False,
                                            False,
                                            True,
                                            True,
                                            False,
                                            False,
                                        ]
                                    },
                                    {"title": "SMA_10 and SMA_50"},
                                ],
                            ),
                            dict(
                                label="SMA_25 and SMA_50",
                                method="update",
                                args=[
                                    {
                                        "visible": [
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                        ]
                                    },
                                    {"title": "SMA_25 and SMA_50"},
                                ],
                            ),
                            dict(
                                label="BOL_upper & BOL_middle & BOL_lower",
                                method="update",
                                args=[
                                    {
                                        "visible": [
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                        ]
                                    },
                                    {"title": "BOL_upper & BOL_middle & BOL_lower"},
                                ],
                            ),
                            dict(
                                label="STO_slowk & STO_slowd",
                                method="update",
                                args=[
                                    {
                                        "visible": [
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                        ]
                                    },
                                    {"title": "STO_slowk & STO_slowd"},
                                ],
                            ),
                            dict(
                                label="RSI",
                                method="update",
                                args=[
                                    {
                                        "visible": [
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            False,
                                            False,
                                            False,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                        ]
                                    },
                                    {"title": "RSI"},
                                ],
                            ),
                            dict(
                                label="MACD & MACD_signal",
                                method="update",
                                args=[
                                    {
                                        "visible": [
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            True,
                                            True,
                                            False,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                        ]
                                    },
                                    {"title": "MACD"},
                                ],
                            ),
                            dict(
                                label="All",
                                method="update",
                                args=[
                                    {
                                        "visible": [
                                            True,
                                            True,
                                            True,
                                            True,
                                            True,
                                            True,
                                            True,
                                            True,
                                            True,
                                            True,
                                            True,
                                            True,
                                            True,
                                            True,
                                            True,
                                            False,
                                            True,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                            False,
                                        ]
                                    },
                                    {"title": "All"},
                                ],
                            ),
                        ],
                        direction="down",
                        pad={"r": 10, "t": 10},
                        showactive=True,
                        x=1,
                        xanchor="left",
                        y=1.1,
                        yanchor="top",
                    )
                ]
            )

            fig.update_layout(height=800)
            # plt_div = plot(fig, output_type='div')
            # return fig.show()
            # print(plt_div)
            # return plt_div
            return fig.to_html()


if __name__ == "__main__":
    tickers = ["GOOG", "TSLA", ""]
    volatile_tickers = ["ROST", "CNEY"]
    average = MovingAverageDayTrading(
        volatile_tickers[0], stop_loss=0.03, take_profit=0.15
    )
    start = time.time()
    average.moving_average_timeframes()
    finish = time.time()
    print(finish - start)

    # ticker = yf.Ticker('GOOG')
    # print(ticker.fast_info.currency)
