import yfinance as yf
import pandas as pd

dataF = yf.download("EURUSD=X", start="2022-10-4", end="2022-12-2", interval='15m')

dataF.iloc[-1:,:]
dataF.Open.iloc

#Define your signal function
# For ingufing patterns
def signal_generator(df):
    open = df.Open.iloc[-1]
    close = df.Close.iloc[-1]

    previous_open = df.Open.iloc[-2]
    previous_close = df.Close.iloc[-2]

    #Bearish Pattern 
    if (open>close and previous_open<previous_close and close<previous_open and open>=previous_close): 
        return 1 

    # Bullish Pattern
    if (open<close and previous_open>previous_close and close>previous_open and open<=previous_close):
        return 2 

    #no clear pattern
    else:
        return 0

    signal = []
    signal.append(0)
    for i in range(1,len(dataF)):
        df = dataF[i-1:i+1]
        signal.append(signal_generator(df))
    #signal_generator(data)
    dataF["signal"] = signal

dataF.signal.value_counts()
#dataF.iloc[:, :]

#connect to the market and execute trades
from apscheduler.schedulers.blocking import BlockingScheduler
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest
from oanda_candles import Pair,Gran, CandleCollector, CandleClient
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails

from config import access_token, aacountID
def get_candles(n):
    #access_token='XXXX' #you need token here generated from OANDA account 
    client = CandleClient(access_token,real=false) # for fake account
    collector = client.get_collector(Pair.EUR_USD, Gran.M15)
    candles = collector.grab(n)
    return candles

candles = get_candles(3)
for candle in candles:
    print(float(str(candle.bid.o)) > 1)


def trading_job():
    candles = get_candles(3)
    dfstream = pd.DataFrame(columns=['Open','Close','High','Low'])

    i = 0
    for candle in candles:
        dfstream.loc[i, ['Open']] = float(str(candle.bid.o))
        dfstream.loc[i, ['Close']] = float(str(candle.bid.c))
        dfstream.loc[i, ['High']] = float(str(candle.bid.h))
        dfstream.loc[i, ['Low']] = float(str(candle.bid.l))
        i =+ 1

    dfstream['Open'] = dfstream['Open'].astype(float)
    dfstream['Close'] = dfstream['Close'].astype(float)
    dfstream['High'] = dfstream['High'].astype(float)
    dfstream['Low'] = dfstream['Low'].astype(float)

    signal = signal_generator(dfstream.iloc[:-1,:])

    #