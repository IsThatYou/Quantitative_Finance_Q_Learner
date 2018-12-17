"""Slice and plot"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range."""
    df = df[columns]
    df = df.ix[start_index:end_index]
    plot_data(df, "lal")


def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def sharpe(alloc, data):
    dr = compute_daily_returns(data)

    for i in range(len(alloc)):
        dr.iloc[:,i] = alloc[i] * dr.iloc[:,i]

    dr_sum = np.sum(dr, axis = 1)
    means = np.mean(dr_sum)
    std = dr_sum.std()
    sharpe = means/std * np.sqrt(251)
    return sharpe
def average_daily_return(alloc,data):
    dr = compute_daily_returns(data)
    for i in range(len(alloc)):
        dr.iloc[:,i] = alloc[i] * dr.iloc[:,i]
    result = np.mean(np.mean(dr))
    return result
def cumulative_return(alloc, data):
    dr = compute_daily_returns(data)
    for i in range(len(alloc)):
        dr.iloc[:,i] = alloc[i] * dr.iloc[:,i]
    result = np.sum(np.sum(dr))
    return result
def volatility(alloc, data):
    dr = compute_daily_returns(data)
    for i in range(len(alloc)):
        dr.iloc[:,i] = alloc[i] * dr.iloc[:,i]
    dr_sum = np.sum(dr, axis = 1)
    std = dr_sum.std()
    return std







def get_data(syms, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    symbols = np.copy(syms)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols = np.insert(symbols, -1, 'SPY')


    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax


###############################second week

def get_rolling_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    return pd.rolling_mean(values, window=window)

def get_ac_mean_ratio(values, window):
    """Return rolling mean of given values, using specified window size."""
    mean = pd.rolling_mean(values, window=window)
    print values[window:]
    return values[window:]/mean[1:]

def get_ac_mean_ratio2(values, window):
    """Return rolling mean of given values, using specified window size."""
    mean = pd.rolling_mean(values, window=window)
    return values/mean[1:]


def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    return pd.rolling_std(values, window=window)


def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    upper_band = rm + 2 * rstd
    lower_band = rm - 2 * rstd
    return upper_band, lower_band

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    # Note: Returned DataFrame must have the same number of rows
    return df[1:].values/df[:-1] - 1

def fill_missing_values(df_data):
    """Fill missing values in data frame, in place."""

    df_data.fillna(method = "ffill", inplace=True)
    df_data.fillna(method = "bfill", inplace=True)
    return df_data
    ##########################################################

def test_run():
    # Define a date range
    dates = pd.date_range('2010-01-01', '2010-12-31')

    # Choose stock symbols to read
    symbols = ['GOOG', 'IBM', 'GLD']  # SPY will be added in get_data()

    # Get stock data
    df = get_data(symbols, dates)

    # Slice and plot
    plot_selected(df, ['SPY', 'IBM'], '2010-03-01', '2010-04-01')


if __name__ == "__main__":
    test_run()
