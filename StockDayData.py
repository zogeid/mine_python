from StockDay import *


class StockDayData(StockDay):
    def __init__(self, is_support=None, is_resistance=None):
        super().__init__()
        self.is_support = is_support
        self.is_resistance = is_resistance
