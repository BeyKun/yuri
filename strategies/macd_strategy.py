"""
MACD Strategy
"""

import numpy, talib


class MACDStrategy:
    def __init__(self, data, fastperiod = 12, slowperiod=26, signalperiod = 9):
        self.macd, self.macdsignal, self.macdhist = talib.MACD(numpy.array(data), fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
        self.FAST_PERIOD = fastperiod
        self.SLOW_PERIOD = slowperiod
        self.SIGNAL_PERIOD = signalperiod

    def crossUp(self):
        if not numpy.isnan(self.macd[-1]) and not numpy.isnan(self.macdsignal[-1]):
            if self.macd[-3] < self.macdsignal[-3] and self.macd[-2] >= self.macdsignal[-2] and self.macd[-1] > self.macdsignal[-1]:
                return True
        return False
    def crossDown(self):
        if not numpy.isnan(self.macd[-1]) and not numpy.isnan(self.macdsignal[-1]):
            if self.macd[-3] > self.macdsignal[-3] and self.macd[-2] <= self.macdsignal[-2] and self.macd[-1] < self.macdsignal[-1]:
                return True
        return False