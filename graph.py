import pandas as pd
from data import Data
from matplotlib import pyplot as plt
from pylab import rcParams
from datetime import date


class Graph:

    def __init__(self, data, x, symbol, description):
        """Initialize variables and plot size
        """
        rcParams["figure.figsize"] = 14, 10
        self.data = data
        self.x = x
        self.red = "#E27E7E"
        self.green = "#6ABDAB"
        self.symbol = symbol
        self.description = description

    def create(self):
        """Create boxplot of existing data columns
        """
        fig, ax = plt.subplots(nrows=2, sharex=True, gridspec_kw={
                               'height_ratios': [6, 1]})
        # Check for existing data to plot
        if "6. mean" in self.data:
            ax[0].plot(self.x, self.data["6. mean"],
                       label="Mean", color="#E6E6E6")
        if "7. low_trend" in self.data:
            ax[0].plot(self.x, self.data["7. low_trend"],
                       label="Low", color="#E8C7C7")
        if "8. high_trend" in self.data:
            ax[0].plot(self.x, self.data["8. high_trend"],
                       label="High", color="#ACC8C2")
        if "9. sma" in self.data:
            ax[0].plot(self.x, self.data["9. sma"],
                       label="SMA 15", color="#F7AE7E")
        if "10. ema" in self.data:
            ax[0].plot(self.x, self.data["10. ema"],
                       label="EMA 100", color="#B9B1F9")
        if set(["1. open", "2. high", "3. low", "4. close"]).issubset(self.data):
            boxplot = ax[0].boxplot(self.data[["1. open", "2. high", "3. low", "4. close"]],
                                    labels=self.x, positions=range(len(self.data)), patch_artist=True)
            for box in range(len(self.data.index)):
                if (self.data.iloc[box, 0] - self.data.iloc[box, 3]) >= 0:
                    plt.setp(boxplot["boxes"][box], color=self.red)
                else:
                    plt.setp(boxplot["boxes"][box], color=self.green)
        # Configure x axis labels
        for index, label in enumerate(ax[1].xaxis.get_ticklabels()):
            if index % 5 != 0:
                label.set_visible(False)
        plt.figtext(0.125, .02, self.description)
        # Description
        ax[1].bar(self.x, self.data["5. volume"], color="#E6E6E6")
        ax[0].set_title("Stock: {}".format(self.symbol))
        ax[0].legend()
        ax[0].yaxis.set_label_position("right")
        ax[0].yaxis.tick_right()
        ax[1].yaxis.set_label_position("right")
        ax[1].yaxis.tick_right()
        ax[0].spines['top'].set_visible(False)
        ax[0].spines['left'].set_visible(False)
        ax[1].spines['top'].set_visible(False)
        ax[1].spines['left'].set_visible(False)
        ax[1].spines['bottom'].set_color('#505050')
        ax[0].spines["right"].set_color('#505050')
        ax[1].spines["right"].set_color('#505050')
        ax[1].tick_params(axis='x', colors='#505050')
        ax[1].tick_params(axis='y', colors='#505050')
        ax[0].tick_params(axis='y', colors='#505050')
        plt.subplots_adjust(wspace=0, hspace=0)
        plt.show()
        fig.savefig("./plots/{}_{}.png".format(
            date.today().strftime("%Y%m%d"), self.symbol), dpi=300)
