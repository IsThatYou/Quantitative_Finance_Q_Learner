import numpy as np
import scipy

class LinRegLearner:
    def __init__():
        pass
    def train(self, X, Y):
        self.m, self.b = scipy.stats.linregress(X, Y)
    def query(self, X):
        y = self.m * X + self.b
        return y


