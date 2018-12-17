
import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.num_states = num_states
        self.s = 0
        self.a = 0
        self.rar = rar
        self.radr = radr
        self.Q = np.random.uniform(low=-1.0, high=1.0, size=(num_states, num_actions))
        self.gamma = gamma
        self.alpha = 0.2
        self.reward = 0
        self.maxu = 0
        self.actions = []

        self.dyna = dyna
        self.t_c = np.ones((num_states, num_actions, num_states))*0.00001
        self.t = np.ones((num_states, num_actions, num_states))*0.00001
        self.r = np.zeros((num_states, num_actions))

        for i in range(self.num_actions):
            self.actions.append(i)

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        action = max(self.Q[self.s])
        number = np.random.random_sample()
        if number < self.rar:
            action = rand.randint(0, self.num_actions-1)
        else:
            action = self.Q[self.s, :].argmax()
        self.rar *= self.radr
        if self.verbose: print "s =", s,"a =",action
        self.a = action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        ## still something needed to be solved.  Need to solve the returning problem.
        #  sometimes it just skyrockets to over 5000
        q_table = self.Q
        self.reward = r
        randomness = rand.random()

        maxu = self.Q[s_prime][self.Q[s_prime,:].argmax()]
        self.maxu = maxu
        reward = self.alpha * r + self.alpha * self.gamma * maxu
        self.Q[self.s][self.a] = (1-self.alpha) * self.Q[self.s][self.a] + reward
        action = self.Q[s_prime, :].argmax()

        ## need to clean this code
        if self.rar >= randomness:
            action = rand.randint(0, self.num_actions-1)
            self.s = s_prime
            self.a = action
            self.rar = self.rar * self.radr
            return action

        self.rar = self.rar * self.radr
        if self.verbose: print "s =", s_prime,"a =",action,"r =",r


        ## dyna part:
        a_temp = self.a

        # check for dyna and build T & R
        if self.dyna > 0:
            self.t_c[self.s][a_temp][s_prime] += 1
            total_count = (self.t_c[self.s][a_temp]).sum()
            self.t[self.s][a_temp][s_prime] = self.t_c[self.s][a_temp][s_prime]/total_count
            self.r[self.s][a_temp] = (1 - self.alpha)*(self.r[self.s][a_temp]) + self.alpha*r

        self.s = s_prime
        self.a = action

        # Start Hallucinations
        if self.dyna > 0:
            for count in range(0, self.dyna):
                s_temp = rand.randint(0, self.num_states-1)
                a_temp = rand.randint(0, self.num_actions-1)
                s_temp_prime = (self.t[s_temp][a_temp]).argmax()
                r_temp = self.r[s_temp][a_temp]
                aa_prime = q_table[s_temp_prime, :].argmax()

                self.Q[s_temp][a_temp] = (1 - self.alpha)*q_table[s_temp][a_temp] + self.alpha*(r_temp+  + self.gamma*q_table[s_temp_prime][aa_prime])

        return action
    def get_q(self):
        return self.Q, self.rar, self.reward,self.maxu






if __name__=="__main__":
    print "Nope"
