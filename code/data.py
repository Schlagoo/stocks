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
        std = self.data["2. high"].std()
        self.data["8. high_trend"] = x
        self.data["8. high_trend"] = self.data["8. high_trend"] * \
            slope + intercept + std

    def get_low(self):
        """Calculate low trend regression
        """
        x = list(range(len(self.x)))
        slope, intercept, _, _, _ = stats.linregress(
            x, self.data["3. low"])
        std = self.data["3. low"].std()
        self.data["7. low_trend"] = x
        self.data["7. low_trend"] = self.data["7. low_trend"] * \
            slope + intercept - std

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
        self.data["9. sma15"] = self.data["4. close"].rolling(window=15).mean()

    def get_ema(self):
        """Calculate expontential moving average by 100 days offset
        """
        self.data["10. ema100"] = self.data["4. close"].ewm(
            span=100, adjust=False).mean()

    def get_bollinger_band(self):
        """Calculate bollinger band based on SMA 20 and k * std.
        If price is normally distributed, probability to be in between band is 95,4 %.
        """
        k = 2
        self.sma20 = round(
            self.data["4. close"].rolling(window=20).mean())
        self.data["11. bollinger up"] = self.sma20 + \
            (k * self.data["4. close"].std())
        self.data["12. bollinger low"] = self.sma20 - \
            (k * self.data["4. close"].std())

    def check_for_price_crossover(self, window=5) -> str:
        """Compare SMA 50 to stock close values to look for price crossovers
        """
        index, trend, price = 0, [], "no"
        sma50 = self.data["4. close"].rolling(window=50).mean().tail(5)
        for _, row in self.data.iloc[-window:].iterrows():
            # SMA 50 above close value
            if (sma50[-window+index]) >= row["4. close"]:
                trend.append(1)
            # SMA 50 below close value
            else:
                trend.append(0)
            index += 1
        # Check for price crossover
        if (sum(trend) % len(trend) != 0):
            price = "bullish" if trend[-1] == 1 else "bearish"

        return price

    def check_for_cross(self, window=5) -> str:
        """Weekly check for golden- or death cross. Default last 5 workdays
        """
        trend = []
        cross = "no"
        for _, row in self.data.iloc[-window:].iterrows():
            # short-therm MA above long-therm MA
            if (row["9. sma15"] >= row["10. ema100"]):
                trend.append(0)
            # short-therm MA below long-therm MA
            else:
                trend.append(1)
        # Check for cross
        if (sum(trend) % len(trend) != 0):
            cross = "golden" if trend[-1] == 0 else "death"

        return cross

    def get_finonacci_retracement(self):
        """Generate fibonacci retracements based on ratios
        """
        ratios = [0, 0.236, 0.382, 0.618, 1]
        min_value = self.data["4. close"].min()
        max_value = self.data["4. close"].max()
        difference = max_value - min_value
        levels = []
        # Generate levels based on difference multiplied by fibonacci ratios
        for ratio in ratios:
            levels.append(round(max_value - (difference * ratio), 2))

        return levels
