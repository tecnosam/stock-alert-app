import pandas as pd
import yfinance as yf

h = pd.read_csv("stocks.csv")
res = []
for i in len( h ):
    tick = yf.Ticker( h.loc[i][''] )