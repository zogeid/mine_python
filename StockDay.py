class StockDay:
    def __init__(self, day=None, apertura=None, max=None, min=None, cierre=None, ajustado=None, volumen=None,
                 cantidaddividendo=None):
        self.date = day
        if apertura is not None:
            self.open = float(apertura)
        if max is not None:
            self.high = float(max)
        if min is not None:
            self.low = float(min)
        if cierre is not None:
            self.close = float(cierre)
        if ajustado is not None:
            self.adjusted_close = float(ajustado)
        self.volume = volumen
        self.dividend_amount = cantidaddividendo

    def imprimir(self):
        print()
        print("day:", self.date)
        print("apertura:", self.open)
        print("max:", self.high)
        print("min:", self.low)
        print("cierre:", self.close)
        print("ajustado:", self.adjusted_close)
        print("volumen:", self.volume)
        print("cantidaddividendo:", self.dividend_amount)
