from ext.utils import *
import sys, os
import numpy as np
import pandas as pd
import yfinance as yf
from threading import Thread, Event
from api import SellingConditions, TradingConditions, BuyingConditions, fetch_user_data
from notifications import Notification
# from ext.quantum_classifier import self.exec_sql
import requests
from db.mysql import Connection
import datetime

class Watch:
    def __init__(self):
        print("#> INITIALIZING STOCK API PIPELINE ")
        [self.sell,self.buy,self.trade] = [SellingConditions(),TradingConditions(),BuyingConditions()]
        self.notif = Notification()
        self.prev_hist = {}
        self.complist = pd.Series( open("symbols.txt", "r").readlines() )
        # self.complist = pd.read_csv('companylist.csv')
        tolower = lambda x: x.lower().strip()
        # self.tickers = ['msft']
        self.db = Connection()
        self.tickers = self.complist.apply( tolower )
        th = Thread(target = self.main, args = ())
        th.daemon = True
        th.start()
        print("### STOCK API PIPELINE RUNNING ON %s " % th)
    def main(self, stock = "*"):
        run_event = Event()
        run_event.set()
        while True:
            try:
                for i in self.tickers:
                    try:
                        ticker = yf.Ticker(i)
                        hist = ticker.history(period = "min")
                    except:
                        continue
                    # hist = pd.read_csv("ext/dat.csv")
                    hist.pop("Volume")
                    if (i not in self.prev_hist):
                        if ( len(hist) > 0 ):
                            self.resolve_movers(hist, i)
                            self.prev_hist[i] = hist.iloc[-1].to_dict()
                        else:
                            self.handle_delisted( i )
                    else:
                        if ( hist.iloc[-1].to_dict() != self.prev_hist[i] ):
                            if ( len(hist) > 0 ):
                                self.resolve_movers(hist, i)
                                self.prev_hist[i] = hist.iloc[-1].to_dict()
                            else:
                                self.handle_delisted( i )
            except KeyboardInterrupt:
                print("#> TERMINATING STOCK API PIPELINE... ")
                run_event.clear()
                print("### TERMINATION SUCCESSFUL ")
                sys.exit()
            except requests.exceptions.ConnectionError:
                print("### COULD NOT CONNECT TO STOCK MARKET API\n#> RETRYING... ")

    def handle_delisted(self, symbol = ""):
        # method to resolve those that have seen their conditions
        # info = ticker.info
        selling = self.exec_delisted( 'sell',symbol )
        buying = self.exec_delisted( 'buy', symbol )
        trading = self.exec_delisted( 'trade', symbol )
        # print("Sellers: ", selling)
        # print("Buyers: ", buying)
        # print("Others: ", trading)

        t1 = Thread(target = self.notif.bulk, args = (selling, symbol, 'delisted'))
        t1.start()
        t2 = Thread(target = self.notif.bulk, args = (buying, symbol, 'delisted'))
        t2.start()
        t3 = Thread(target = self.notif.bulk, args = (trading, symbol, 'delisted'))
        t3.start()
    def resolve_movers(self, req, symbol = ""):
        # method to resolve those that have seen their conditions
        # info = ticker.info
        selling = self.exec_sql( 'sell', req, symbol )
        buying = self.exec_sql( 'buy', req, symbol, 'less' )
        trading = self.exec_sql( 'trade', req, symbol, 'equal' )
        # print("Sellers: ", selling)
        # print("Buyers: ", buying)
        # print("Others: ", trading)

        t1 = Thread(target = self.notif.bulk, args = (selling, symbol, 'selling'))
        t1.start()
        t2 = Thread(target = self.notif.bulk, args = (buying, symbol, 'buying'))
        t2.start()
        t3 = Thread(target = self.notif.bulk, args = (trading, symbol, 'trade'))
        t3.start()
    def exec_delisted(self, tbl, symb):
        sql = f"SELECT `uid` FROM `%s` WHERE `name`='{symb}'" % tbl
        try:
            uids = self.db.get(sql)
            self.db.set(f"DELETE FROM `%s` WHERE `name`='{symb}'" % tbl)
            return uids
        except Exception as e:
            raise e
    def exec_sql( self, tbl, req, symbol, arith_meth = "greater" ):
        if ( arith_meth == "greater" ):
            sql = """
                        SELECT `uid` FROM `%s` WHERE `open`<=%s AND close<=%s AND high<=%s
                        AND low<=%s AND dividends<=%s AND splits<=%s AND name='%s'
                """ % ( 
                    tbl, 
                    req.Open.iloc[-1], 
                    req.Close.iloc[-1], 
                    req.High.iloc[-1], 
                    req.Low.iloc[-1], 
                    req.Dividends.iloc[-1], 
                    req['Stock Splits'].iloc[-1], symbol )
        elif ( arith_meth == "less" ):
            sql = """
                        SELECT `uid` FROM `%s` WHERE `open`>=%s AND close>=%s AND high>=%s
                        AND low>=%s AND dividends>=%s AND splits>=%s AND name='%s'
                """ % ( 
                    tbl, 
                    req.Open.iloc[-1], 
                    req.Close.iloc[-1], 
                    req.High.iloc[-1], 
                    req.Low.iloc[-1], 
                    req.Dividends.iloc[-1], 
                    req['Stock Splits'].iloc[-1], symbol )
        elif ( arith_meth == "equal" ):
            sql = """
                        SELECT `uid` FROM `%s` WHERE `open`=%s AND close=%s AND high=%s
                        AND low=%s AND dividends=%s AND splits=%s AND name='%s'
                """ % ( 
                    tbl, 
                    req.Open.iloc[-1], 
                    req.Close.iloc[-1], 
                    req.High.iloc[-1], 
                    req.Low.iloc[-1], 
                    req.Dividends.iloc[-1], 
                    req['Stock Splits'].iloc[-1], symbol )
        try:
            return self.db.get( sql )
        except Exception as e:
            print(req)
            raise e
    # def resolve_victims(self, req, ticker):
    #     info = ticker.info
    #     selling = self.exec_sql(req, self.sell.bidders( info['symbol'] ))
    #     buying = self.exec_sql(req, self.buy.bidders( info['symbol'] ))
    #     trading = self.exec_sql(req, self.trade.bidders( info['symbol'] ))

    #     t1 = Thread(self.notif.bulk, (selling, "suggest change sell"))
    #     t1.start()
    #     t2 = Thread(self.notif.bulk, (buying, "suggest change buy"))
    #     t2.start()
    #     t3 = Thread(self.notif.bulk, (trading, "suggest change alert"))
    #     t3.start()
        # method to resolve those that probably have not seen any of their conditions match in a while

# import yfinance as yf

# msft = yf.Ticker("MSFT")
# print(msft)
"""
returns
<yfinance.Ticker object at 0x1a1715e898>
"""

# get stock info
# msft.info

"""
returns:
{
 'quoteType': 'EQUITY',
 'quoteSourceName': 'Nasdaq Real Time Price',
 'currency': 'USD',
 'shortName': 'Microsoft Corporation',
 'exchangeTimezoneName': 'America/New_York',
  ...
 'symbol': 'MSFT'
}
"""
# get historical market data, here max is 5 years.
# msft.history(period="max")
"""
returns:
              Open    High    Low    Close      Volume  Dividends  Splits
Date
1986-03-13    0.06    0.07    0.06    0.07  1031788800        0.0     0.0
1986-03-14    0.07    0.07    0.07    0.07   308160000        0.0     0.0
...
2019-11-12  146.28  147.57  146.06  147.07    18641600        0.0     0.0
2019-11-13  146.74  147.46  146.30  147.31    16295622        0.0     0.0
"""