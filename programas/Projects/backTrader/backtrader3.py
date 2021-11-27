# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 19:57:31 2021

@author: INNOVACION
"""

import datetime

import backtrader as bt

#from backtrader_plotting import Bokeh
import matplotlib


class TestStrategy(bt.Strategy):
    params = (
        ('buydate', 12),
        ('holdtime', 4),
        ('today',0)
    )

    def next(self):
        var1=len(self.data)
        var2=self.p.buydate
        var3= self.p.holdtime
        if len(self.data) == (self.p.buydate +self.p.today):
            self.buy(self.datas[0], size=None)

        if len(self.data) == self.p.buydate + self.p.holdtime:
            self.sell(self.datas[0], size=None)
            self.p.today = len(self.data)


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy, buydate=3)

    data = bt.feeds.YahooFinanceCSVData(
        dataname="oracle.csv",
        # Do not pass values before this date
        fromdate=datetime.datetime(2000, 1, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2001, 2, 28),
        reverse=False,
        )
    cerebro.adddata(data)
    
    ## salvamos en un fichero
    cerebro.addwriter(bt.WriterFile, csv=True, out='bcktrader3_v1.csv')    

    cerebro.run()

    #Los ploteados mejor en jupyter
    #b = Bokeh(style='bar', plot_mode='single')
    #cerebro.plot(b)