import numpy
import matplotlib.pyplot as plt
import pandas as pd

def test_run ():
    df = pd.read_csv("data/GOOG.csv")
    print df.head()
    print df['Close'].max()

if __name__=="__main__":
    test_run()

