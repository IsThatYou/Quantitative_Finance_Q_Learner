import StrategyLearner3 as sl
import datetime as dt
import utility
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
##from matplotlib.font_manager import FontProperties


sd = dt.datetime(2010,1,1)
ed = dt.datetime(2010,12,31)

symbol = "GLD"
learner = sl.StrategyLearner(symbols=[symbol],\
                             sd = sd,\
                             ed = ed,\
                             sv = 100000, \
                             verbose = False) # constructor
result = learner.train()

dates = pd.date_range(sd, ed)
stocks = utility.get_data(symbol, dates)
prices = pd.DataFrame(np.zeros(((ed-sd).days + 1,1)))
prices.columns = [symbol]
result = np.zeros((251,1)) + 10
portfolio = 0
inv = 0
out = 100000



####3

value = 100000
money = True
for i in range(0, 250):
    prices[symbol].iloc[i] = stocks[symbol].iloc[i]
    if i >14:
        fiftendays = prices[symbol].loc[i-14:i]
        ac_mean = utility.get_ac_mean_ratio2(fiftendays, 15).iloc[-1]

        action = learner.query(i, ac_mean, money)
        if action == 0:
            if 100 * prices[symbol].iloc[i] > value:
                money = False
                action = learner.query(i, ac_mean, money)
            else:
                portfolio += 100
                money = True
                value -= 100 * prices[symbol].iloc[i]

        if action == 1:
            if portfolio < 10:
                money = False
                action = learner.query(i, ac_mean, money)
            if portfolio >= 100:
                portfolio -= 100
                Money = True
                value += 100 * prices[symbol].iloc[i]
        result[i] = action

####2
'''
value = 100000
money = True
for i in range(0, 250):
    prices[symbol].iloc[i] = stocks[symbol].iloc[i]
    if i >19:
        tendays = prices[symbol].loc[i-9:i]
        twentydays = prices[symbol].loc[i-19:i]
        tenmean = utility.get_rolling_mean(tendays, 10).iloc[-1]
        twentymean = utility.get_rolling_mean(twentydays, 20).iloc[-1]
        dr = utility.compute_daily_returns(tendays).iloc[-1]

        action = learner.query(i, dr, tenmean, twentymean, money)
        if action == 0:
            if 100 * prices[symbol].iloc[i] > value:
                money = False
                action = learner.query(i, dr, tenmean, twentymean, money)
            else:
                portfolio += 100
                money = True
                value -= 100 * prices[symbol].iloc[i]

        if action == 1:
            if portfolio < 10:
                money = False
                action = learner.query(i, dr, tenmean, twentymean, money)
            if portfolio >= 100:
                portfolio -= 100
                Money = True
                value += 100 * prices[symbol].iloc[i]


        result[i] = action

volumn = 100000/stocks[symbol].iloc[0]
initial = volumn * stocks[symbol].iloc[0]
left = 100000 - initial
final = volumn * stocks[symbol].iloc[-1]
benchmark = final + left
print "benchmark:" + str(benchmark)
'''

'''
###4
value = 100000
money = True
for i in range(0, 250):
    prices[symbol].iloc[i] = stocks[symbol].iloc[i]
    if i >14:
        fiftendays = prices[symbol].loc[i-14:i]
        ac_mean = utility.get_ac_mean_ratio(fiftendays, 15).iloc[-1]
        rm = utility.get_rolling_mean(fiftendays, 15)
        rstd = utility.get_rolling_mean(fiftendays, 15)
        #only using the up value
        bband_up, bband_down = utility.get_bollinger_bands(rm, rstd)
        bband_up = bband_up.iloc[-1]
        action = learner.query(i, bband_up, money)
        if action == 0:
            if 100 * prices[symbol].iloc[i] > value:
                money = False
                action = learner.query(i, bband_up, money)
            else:
                portfolio += 100
                money = True
                value -= 100 * prices[symbol].iloc[i]

        if action == 1:
            if portfolio < 10:
                money = False
                action = learner.query(i,bband_up, money)
            if portfolio >= 100:
                portfolio -= 100
                Money = True
                value += 100 * prices[symbol].iloc[i]


        result[i] = action
'''

for i in range(len(result)):
    if result[i] == 0:
        result[i] = 100
    elif result[i] == 1:
        result[i] = -100
    elif result[i] == 2:
        result[i] = 0
print result
test = utility.plot_data(stocks)




count = 0
counts = 0
X=[]
Y=[]
X2 = []
Y2 = []
for i in range(1, len(stocks.index)-1):
    if result[i] == 100:
        inv = inv + 100
        out = out - 100 * stocks[symbol].iloc[i]
        X.append(stocks.index.values[i])
        Y.append(stocks[symbol].iloc[i])


    if result[i] == -100:

        inv = inv - 100
        out = out + 100 * stocks[symbol].iloc[i]
        X2.append(stocks.index.values[i])
        Y2.append(stocks[symbol].iloc[i])


plt.plot(X, Y, marker='o', color='r', ls='', label="Buy")
plt.plot(X2, Y2, marker='o', color='b', ls='', label="Sell")
plt.legend(bbox_to_anchor=(1.15, 0.5))



total = inv * stocks[symbol].iloc[-1] + out
print inv, out
print total
print portfolio


plt.show()




#learner.addEvidence(symbol = "IBM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), sv = 10000) # training step
#df_prices = learner.testPolicy(symbol = "IBM", sd=dt.datetime(2009,1,1), ed=dt.datetime(2010,1,1), sv = 10000) # testing step

