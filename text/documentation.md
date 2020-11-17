# Documentation

This document should serve as a documentation of implemented techniques for statistical analysis of stock charts.

### Box-Cox Plot

Stock charts is used to display data values where one is interested in 4 different values for each data point. This could for example be used to display a stock's open,close, min and max value during a specific day. [Source](http://www.digialliance.com/docs/jpgraph/html/3055stockplot.html)

### Trends

The first step is to identify the overall trend. This can be accomplished with trend lines. For example, the trend is up as long as price remains above its upward sloping trend line or a certain moving average. Similarly, the trend is up as long as higher troughs form on each pullback and higher highs form on each advance. [Source](https://school.stockcharts.com/doku.php?id=overview:technical_analysis)

##### Mean

Mean trend shows general tendency of price development. It is calculated by linear regression of a stock's close data to derive slope and intercept.

Formula:
$$
M = slope * x + intercept
$$

##### High, low

High and low trends show tendency of a stock's high and low performance. It can be calculated by linear regression of a stock's high/low values too.

Formula:
$$
H/L = slope * x + intercept
$$

### Moving Averages

The percentage of stocks trading above a specific moving average is a breadth indicator that measures internal strength or weakness in the underlying index. The 50-day moving average is used for short-to-medium-term timeframes, while the 150-day and 200-day moving averages are used for medium-to-long-term timeframes. Signals can be derived from overbought/oversold levels, crosses above/below 50% and bullish/bearish divergences. [Source](https://school.stockcharts.com/doku.php?id=market_indicators:percent_above_ma)

##### Simple Moving Average (SMA)

A simple moving average is formed by computing the average price of a security over a specific number of periods. Most moving averages are based on closing prices; for example, a 5-day simple moving average is the five-day sum of closing prices divided by five. As its name implies, a moving average is an average that moves. Old data is dropped as new data becomes available, causing the average to move along the time scale. [Source](https://school.stockcharts.com/doku.php?id=technical_indicators:moving_averages)

Formula:
$$
SMA_n = \frac{d_1, d_2, ..., d_n}{n}
$$

##### Exponential Moving Average (EMA)

The exponential moving average is a type of moving average that gives more weight to recent prices in an attempt to make it more responsive to new information. To calculate an EMA, you must first compute the simple moving average (SMA) over a particular time period. Next, you must calculate the multiplier for weighting the EMA (referred to as the "smoothing factor"). Then you use the smoothing factor combined with the previous EMA to arrive at the current value. The EMA thus gives a higher weighting to recent prices, while the SMA assigns equal weighting to all values. [Source](https://school.stockcharts.com/doku.php?id=technical_indicators:moving_averages)

Formula:
$$
EMA_n (t) = \alpha * x(t) + (1-\alpha) * EMA_n(t - 1)
$$

### Bollinger-Band

Chart analysis procedure. Based on the normal distribution, it is assumed that current prices of a security are more likely to be close to the mean value of past prices than far away from it. Chart analysis procedure. Based on the normal distribution, it is assumed that current prices of a security are more likely to be close to the mean value of past prices than far away from it. [Source](https://de.wikipedia.org/wiki/Bollinger-B%C3%A4nder)

Formulas:
$$
BB_{m} = \bar C_t = \frac{\sum_{i=1}^{n-1}C_{t-i}}{n}
$$

$$
BB_{u} = C_{t-i} + k * \sigma_t
$$

$$
BB_{l} = C_{t-i} - k * \sigma_t
$$

The factor k in conjunction with the standard deviation controls the width of the gap between upper and lower band. Assuming that the rates of the next time step (t+1) are random and normally distributed, the rate is found with a probability dependent on k within the band gap between upper and lower band. For example, with a factor of 2, this probability is 95.4 %.

### Fibonacci Retracement

### Price crossover

### Golden/Death cross

