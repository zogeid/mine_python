class StockDay:
    def __init__(self, date=None, open=None, high=None, low=None, close=None, adjusted_close=None, volume=None,
                 dividend_amount=None):
        self.date = date
        self.volume = volume
        self.dividend_amount = dividend_amount

        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.adjusted_close = None

        if open is not None:
            self.open = float(open)
        if high is not None:
            self.high = float(high)
        if low is not None:
            self.low = float(low)
        if close is not None:
            self.close = float(close)
        if adjusted_close is not None:
            self.adjusted_close = float(adjusted_close)

    def print(self):
        print()
        print("Fecha:", self.date)
        print("Apertura:", self.open)
        print("Máximo:", self.high)
        print("Mínimo:", self.low)
        print("Cierre:", self.close)
        print("Ajuste:", self.adjusted_close)
        print("Volumen:", self.volume)
        print("Dividendo:", self.dividend_amount)

    def get_stockday_data(self):
        data = ("Fecha:", self.date, "Apertura:", self.open, "Máximo:", self.high, "Mínimo:", self.low, "Cierre:",
                self.close, "Ajuste:", self.adjusted_close, "Volumen:", self.volume, "Dividendo:", self.dividend_amount)
        return data
