from StockDay import *


class StockDayData(StockDay):
    def __init__(self, stockday, is_support=None, is_resistance=None):
        super().__init__(stockday.date, stockday.open, stockday.high, stockday.low, stockday.close, stockday.adjusted_close, stockday.volume, stockday.dividend_amount)
        self.is_support = is_support
        self.is_resistance = is_resistance

    def print(self):
        super().print()
        # print("Es resistencia:", self.is_resistance)
        print("Es resistencia" if self.is_resistance else "No es resistencia")
        # print("Es soporte:", self.is_support)
        print("Es soporte" if self.is_support else "No es soporte")
