import yfinance as yf
import pandas as pd

dataF = yf.download("EURUSD=X", start="2022-10-4", end="2022-12-2", interval='15m')

dataF.iloc[-1:,:]
dataF.Open.iloc

#Define your signal function
def signal_generator(df):
    open = df.Open.iloc[-1]
    close = df.Close.iloc[-1]

    previous_open = df.Open.iloc[-2]
    previous_close = df.Close.iloc[-2]

    #Bearish Pattern
    if (open>close and previous_open<previous_close and close<previous_open and open>=previous_close):
        return 1