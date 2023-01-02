import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

class MovingAverageDayTrading():

    def __init__(self, ticker):
        self.ticker = ticker

    def moving_average_timeframes(self):
        df = yf.download(self.ticker, start='2022-01-01')
        df['MA5'] = df['Adj Close'].rolling(5).mean()
        df['MA8'] = df['Adj Close'].rolling(8).mean()
        df['MA13'] = df['Adj Close'].rolling(13).mean()

        df = df.dropna()
        df = df[['Adj Close', 'MA5', 'MA8', 'MA13']]

        buy = []
        sell= []
        #thing = df.MA5.iloc[0]

        for i in range(len(df)):
            if df.MA5.iloc[i] > df.MA8.iloc[i] and df.MA5.iloc[i-1] < df.MA8.iloc[i-1]:
                buy.append(i)
            elif df.MA8.iloc[i] > df.MA13.iloc[i] and df.MA8.iloc[i-1] < df.MA13.iloc[i-1]:
                buy.append(i)
            elif df.MA5.iloc[i] < df.MA8.iloc[i] and df.MA5.iloc[i-1] > df.MA8.iloc[i-1]:
                sell.append(i)
            elif df.MA8.iloc[i] < df.MA13.iloc[i] and df.MA8.iloc[i-1] > df.MA13.iloc[i-1]:
                sell.append(i)

        print(sell)
        print(buy)
        plt.figure(figsize=(12,5))
        plt.plot(df['Adj Close'], label= 'Asset price', c='blue', alpha=0.5)
        plt.plot(df['MA5'], label='MA5', c='k', alpha= 0.9)
        plt.plot(df['MA8'], label='MA8', c='magenta', alpha= 0.9)
        plt.plot(df['MA13'], label='MA13', c='yellow', alpha= 0.9)
        plt.scatter(df.iloc[buy].index,df.iloc[buy]['Adj Close'], marker='^', color='g', s=100)
        plt.scatter(df.iloc[sell].index,df.iloc[sell]['Adj Close'], marker='v', color='r', s=100)
        plt.legend()
        return plt.show()

if __name__ == '__main__':
    
    average = MovingAverageDayTrading('GOOG')
    print(average.moving_average_timeframes())

