#!/usr/bin/python3

import pandas as pd
from data import Data
from matplotlib import pyplot as plt
from pylab import rcParams, text
from datetime import date


class Graph:

    def __init__(self, data, x, symbol, levels):
        """Initialize variables and plot size
        """
        rcParams["figure.figsize"] = 14, 10
        self.data = data
        self.x = x
        self.red = "#E27E7E"
        self.green = "#6ABDAB"
        self.symbol = symbol
        self.levels = levels

    def create(self):
        """Create boxplot of existing data columns
        """
        fig, ax = plt.subplots(nrows=2, sharex=True, gridspec_kw={
                               'height_ratios': [6, 1]})
        # Check for existing data to plot
        if self.levels:
            # Plot fibonacci replacements
            ax[0].axhspan(self.levels[0], self.levels[1],
                          alpha=0.1, color="#40E6BF")
            ax[0].text(0.25, self.levels[0] - 0.75, "0.0 %", color="#40E6BF")
            ax[0].axhspan(self.levels[1], self.levels[2],
                          alpha=0.1, color="#DEEA5E")
            ax[0].text(0.25, self.levels[1] - 0.75, "23.6 %", color="#DEEA5E")
            ax[0].axhspan(self.levels[2], self.levels[3],
                          alpha=0.1, color="#E67143")
            ax[0].text(0.25, self.levels[2] - 0.75, "38.2 %", color="#E67143")
            ax[0].axhspan(self.levels[3], self.levels[4],
                          alpha=0.1, color="#E6264D")
            ax[0].text(0.25, self.levels[3] - 0.75, "61.8 %", color="#E6264D")
        if "6. mean" in self.data:
            ax[0].plot(self.x, self.data["6. mean"],
                       label="Mean", color="#E6E6E6")
        if "7. low_trend" in self.data:
            ax[0].plot(self.x, self.data["7. low_trend"],
                       label="Low", color="#E8C7C7")
        if "8. high_trend" in self.data:
            ax[0].plot(self.x, self.data["8. high_trend"],
                       label="High", color="#ACC8C2")
        if "9. sma15" in self.data:
            ax[0].plot(self.x, self.data["9. sma15"],
                       label="SMA 15", color="#F7AE7E")
        if "10. ema100" in self.data:
            ax[0].plot(self.x, self.data["10. ema100"],
                       label="EMA 100", color="#B9B1F9")
        if "11. bollinger up" in self.data and "12. bollinger low" in self.data:
            ax[0].plot(self.x, self.data["11. bollinger up"],
                       label="Bollinger band", color="#D0D0D0")
            ax[0].plot(self.x, self.data["12. bollinger low"], color="#D0D0D0")
            ax[0].fill_between(self.x, self.data["11. bollinger up"],
                               self.data["12. bollinger low"], color="#D0D0D0", alpha=0.25)
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
                if index % 4 != 0:
                    label.set_visible(False)
        # Plot volume
        colors = self.color_bars()
        ax[1].bar(self.x, self.data["5. volume"], color=colors)
        # Description
        ax[0].set_title("Stock: {}".format(self.symbol))
        # ax[0].legend(loc="lower left")
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
        fig.savefig("../imgs/{}_{}.png".format(
            date.today().strftime("%Y%m%d"), self.symbol), dpi=300)

    def color_bars(self):
        """Color volume bars based on if higher than mean
        """
        colors = []
        volume_mean = self.data["5. volume"].mean()
        for entry in self.data["5. volume"].values:
            colors.append("#D0D0D0" if entry > volume_mean else "#E6E6E6")

        return colors
