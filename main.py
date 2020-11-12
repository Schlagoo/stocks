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
            viz = Graph(stock.data, stock.x, symbol, stock.description)
            viz.create()
