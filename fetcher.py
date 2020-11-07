#!/usr/bin/python3

import datetime
from alpha_vantage.timeseries import TimeSeries


API_KEY = "V4M6OKQAKTF3IU2P"
symbols = ["UBER"]


class Fetcher:

	def __init__(self, key, symbols):
		"""Initialize variables and Alpha Vantage API 
		"""
		self.API_KEY = key
		self.symbols = symbols
		self.timeseries = TimeSeries(key=self.API_KEY, output_format="pandas")
		self.get_data()

	def get_data(self):
		"""Fetch data from TimeSeries object
		"""
		#t1 = datetime.date.today()
		#t0 = t1 - datetime.timedelta(days=1)
		# Fetch data and meta data as DataFrame
		data, meta = self.timeseries.get_intraday(symbol=self.symbols[0], interval="1min", outputsize="compact")
		#print(data[data.index].str.contains("2020-11-06"))
		#print(data.index.contains("2020-11-06"))
		# TODO: Fetch only current day
		print(data)


f = Fetcher(API_KEY, symbols)

