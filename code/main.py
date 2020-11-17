#!/usr/bin/python3

from data import Data
from graph import Graph


API_KEY = "SEOC47M8VXQBHO41"
symbols = ["UBER", "MSFT", "DIS"]


class Handler:

    def __init__(self, key, symbols):
        """Initialize variables and instantiate Data and Graph objects
        """
        self.process(key, symbols)

    def process(self, key, symbols):
        """Process and visualize data
        """
        for symbol in symbols:
            stock = Data(key=key, symbol=symbol)
            stock.get_x()
            stock.get_mean()
            stock.get_low()
            stock.get_high()
            stock.get_sma()
            stock.get_ema()
            stock.description = stock.interpret_sma()
            # Create plots
            viz = Graph(stock.data, stock.x, symbol)
            viz.create()
