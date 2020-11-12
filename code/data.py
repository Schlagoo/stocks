#!/usr/bin/python3

import datetime
import pandas as pd
from scipy import stats
from alpha_vantage.timeseries import TimeSeries
from currency_converter import CurrencyConverter


API_KEY = "SEOC47M8VXQBHO41"
symbols = ["UBER"]


class Data:

    def __init__(self, key, symbol):
        """Initialize variables and Alpha Vantage API 
        """
        self.API_KEY = key
        self.symbol = symbol
        self.timeseries = TimeSeries(key=self.API_KEY, output_format="pandas")
        self.fetch()

    def fetch(self):
        """Fetch data from TimeSeries object
        """
        self.data, self.meta = self.timeseries.get_daily(
            symbol=self.symbol, outputsize="compact")
        self.data = self.data.sort_index()
        self.data = self.data[(datetime.date.today(
        )-datetime.timedelta(days=180)):datetime.date.today()]
        self.convert()

    def get_x(self):
        """Get list of stripped timestamps
        """
        self.x = self.data.index.to_list()
        for i, value in enumerate(self.x):
            self.x[i] = str(datetime.datetime.strptime(
                str(value), '%Y-%m-%d %H:%M:%S').date())[5:]

    def convert(self):
        """Convert data from USD to EUR
        """
        converter = CurrencyConverter()
        for column in self.data:
            for i, value in enumerate(self.data[column]):
                self.data[column].iloc[i] = round(
                    converter.convert(value, "USD", "EUR"), 2)

    def get_high(self):
        """Calculate high trend regression
        """
        x = list(range(len(self.x)))
        slope, intercept, _, _, _ = stats.linregress(
            x, self.data["2. high"])
        sd = self.data["2. high"].std()
        self.data["8. high_trend"] = x
        self.data["8. high_trend"] = self.data["8. high_trend"] * \
            slope + intercept + sd

    def get_low(self):
        """Calculate low trend regression
        """
        x = list(range(len(self.x)))
        slope, intercept, _, _, _ = stats.linregress(
            x, self.data["3. low"])
        sd = self.data["3. low"].std()
        self.data["7. low_trend"] = x
        self.data["7. low_trend"] = self.data["7. low_trend"] * \
            slope + intercept - sd

    def get_mean(self):
        """Calculate mean regression
        """
        x = list(range(len(self.x)))
        slope, intercept, _, _, _ = stats.linregress(
            x, self.data["4. close"])
        self.data["6. mean"] = x
        self.data["6. mean"] = self.data["6. mean"] * slope + intercept

    def get_sma(self):
        """Calculate simple moving average by 15 days offset
        """
        self.data["9. sma"] = self.data["4. close"].rolling(window=15).mean()
        self.sma50 = round(self.data["4. close"].tail(50).rolling(
            window=50).mean().iloc[-1], 3)
        self.sma100 = round(self.data["4. close"].tail(100).rolling(
            window=100).mean().iloc[-1], 3)

    def interpret_sma(self):
        """Interpret SMA to indicate buy, hold, sell
        """
        if (self.sma50 > self.data["4. close"].iloc[-1] and self.sma50 < self.data["4. close"].iloc[-2]):
            action = "BUY"
        elif (self.sma50 < self.data["4. close"].iloc[-1] and self.sma50 > self.data["4. close"].iloc[-2]):
            action = "SELL"
        else:
            action = "HOLD"

        return "Stock {}: {}".format(self.symbol, action)

    def get_ema(self):
        """Calculate expontential moving average by 100 days offset
        """
        self.data["10. ema"] = self.data["4. close"].ewm(
            span=100, adjust=False).mean()
