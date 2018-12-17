

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import scipy.optimize as spo
from utility import get_data, plot_data, compute_daily_returns,sharpe, average_daily_return, cumulative_return, volatility

def err(alloc, data):
    dr = compute_daily_returns(data)

    for i in range(len(alloc)):
        dr.iloc[:,i] = alloc[i] * dr.iloc[:,i]

    dr_sum = np.sum(dr, axis = 1)
    means = np.mean(dr_sum)
    std = dr_sum.std()
    sharpe = means/std * np.sqrt(251)
    return -1 * sharpe


def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    allocs = np.ones(len(syms)) # add code here to find the allocations
    constraint = ({ 'type': 'eq', 'fun': lambda inputs: 1.0 - np.sum(inputs) })
    bounds = ((0,2),) * len(syms)
    result = spo.minimize(err, allocs, args=(prices,), method="SLSQP", constraints=constraint,bounds=bounds)
    sddr = 0
    sr = sharpe(result.x, prices)
    allocs = result.x
    adr = average_daily_return(allocs, prices)
    cr = cumulative_return(allocs, prices)
    sddr = volatility(allocs, prices)

    # Get daily portfolio value
    port_val = prices_SPY # add code here to compute daily portfolio values

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        pass

    return allocs, cr, adr, sddr, sr

def test_code():


    start_date = dt.datetime(2010,1,1)
    end_date = dt.datetime(2010,12,31)
    symbols = ['GOOG','AAPL','GLD','XOM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = False)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":

    test_code()
