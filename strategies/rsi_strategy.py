"""
RSI Strategy
"""

import numpy, talib
from traitlets import Bool

class RSIStrategy:
    
    def __init__(self, data = [], period = 14, oversold = 30, overbought = 70):
        self.DATA = talib.RSI(numpy.array(data), timeperiod=period)
        self.PERIOD = period
        self.OVER_SOLD = oversold
        self.OVER_BOUGHT = overbought

    def isOverBought(self) -> Bool:
        if self.DATA[-1] > self.OVER_BOUGHT:
            return True
        
        return False

    def isOverSold(self) -> Bool:
        if self.DATA[-1] < self.OVER_SOLD:
            return True
        
        return False