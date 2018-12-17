

import numpy as np
import random as rand
import QLearner as ql
import utility
import pandas as pd

class StrategyLearner(object):

    def __init__(self, \
        symbols, \
        sd, \
        ed, \
        sv, \
        verbose = False):
        self.symbols = symbols
        self.sd = sd
        self.ed = ed
        self.sv = sv

        self.dates = pd.date_range(sd, ed)
        self.stocks = utility.get_data(self.symbols, self.dates)
        self.tenmean_pd=[]
        self.twentymean_pd=[]
        self.dsharpe_pd = []





    def train(self): ##
        ## add technical features.  Right now: daily return, 15-day mean,(std)
        df = pd.DataFrame(index=self.dates)
        self.rm = utility.get_rolling_mean(self.stocks, 15)
        self.rstd = utility.get_rolling_mean(self.stocks, 15)

        self.bband_up, self.bband_down = utility.get_bollinger_bands(self.rm, self.rstd)
        self.steps = 10
        self.stepsize = int(self.bband_up[self.symbols].count()/self.steps)
        sorted = self.bband_up.sort_values(self.symbols)
        self.threshold1 = np.zeros((10, 1))
        for i in range(0, self.steps):
            self.threshold1[i] = sorted.iloc[:,1][(i+1) * self.stepsize]


        self.q_learner = ql.QLearner(num_states=44,\
        num_actions = 3, \
        rar = 0.98, \
        radr = 0.9999, \
        verbose=False,\
        dyna=0) #initialize the learner
        ##print 1 < (return_pd[self.symbols].count() - 1)
        ##print return_pd[self.symbols].iloc[1]
        for iteration in range(0, 100):
            steps = 20
            totalshares = 0
            data = self.stocks.iloc[:,1].copy()
            ac_mean = 0
            bband = 0
            money = True
            state = self.discretize(bband, money) #convert the features to a state
            action = self.q_learner.querysetstate(state) #set the state and get first action
            while steps < data.count() - 1:

                #move to new location according to action and then get a new action
                state = self.discretize(bband, money)
                # since each buy or sell is of 100 shares.
                # This simulates the buying and selling of stocks through difference of rewards.
                # 0: buy, 1: sell, 2: hold
                r = 0
                if action == 0:
                    if data[steps-1] * 100 < self.sv:
                        r = -10 * data[steps-1] * 100
                        money = False
                    else:
                        r = -1 * data[steps-1] * 100
                        money = True
                if action == 1:
                    if totalshares < 100:
                        money = False
                        r = -10 * data[steps] * 100
                    else:
                        money = True
                        self.sv = self.sv + data[steps] * 100
                        totalshares -= 100
                        r = data[steps] * 100

                action = self.q_learner.query(state,r)


                bband = self.bband_up[self.symbols].iloc[steps].item()


                steps += 1

            print iteration

        pass

    def discretize(self, bband_up, money):
        dr_count = 0

        for i in range(1, self.steps):
            if self.threshold1[i].item(0)>bband_up and bband_up > self.threshold1[i-1].item(0):
                dr_count = i
        if bband_up < self.threshold1[0].item(0):
            dr_count = 0
        if bband_up > self.threshold1[self.steps - 1].item(0):
            dr_count = self.steps


        if money == False:
            dr_count = dr_count + self.steps + 1
        return dr_count
        pass


    def query(self, steps, bband, money):
        state = self.discretize(bband, money)
        print state
        action = self.q_learner.querysetstate(state)
        return action






if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
