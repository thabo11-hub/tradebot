import yfinance as yf
import pandas as pd

dataF = yf.download("EURUSD=X", start="2022-10-4", end="2022-12-2", interval='15m')
dataF.iloc[-1:,:]
dataF.Open.iloc