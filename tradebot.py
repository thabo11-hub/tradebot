import yfinance as yf
import pandas as pd

dataF = yf.download("EURUSD=X", start="2022-10-4", end)