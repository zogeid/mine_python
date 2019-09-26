class StockMetaData:
    def __init__(self, info, symbol, refresh, timezone):
        self.information = info
        self.symbol = symbol
        self.refresh = refresh
        self.timezone = timezone

    def print(self):
        print("Info:", self.information)
        print("Symbol:", self.symbol)
        print("Refresh:", self.refresh)
        print("Timezone:", self.timezone)
