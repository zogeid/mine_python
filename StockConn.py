import requests
from StockDay import StockDay
from StockMetaData import *
from StockDayData import *


class StockConn:

    def __init__(self, base_url=None, function=None, datatype=None, api_key=None, symbol=None):
        self.base_url = base_url
        self.function = function
        self.datatype = datatype
        self.api_key = api_key
        self.symbol = symbol
        self.stock_request = None
        self.historic_data = []
        if self.base_url is not None:
            self.url = self.compose_url()
        self.stock_day_data = []

    def compose_url(self):
        url = self.base_url + '/query?function=' + self.function + '&symbol=' + self.symbol + '&datatype=' + self.datatype + '&apikey=' + self.api_key
        return url

    def connect(self):
        self.stock_request = requests.get(self.url)
        if self.stock_request.status_code == 200:
            print("Connection done!")
            print(self.stock_request.json())

    def get_all_day_data(self):
        result_json = self.stock_request.json()
        return result_json['Weekly Adjusted Time Series']

    def get_metadata(self):
        result_json = self.stock_request.json()
        md = result_json['Meta Data']
        return StockMetaData(md['1. Information'], md['2. Symbol'], md['3. Last Refreshed'], md['4. Time Zone'])

    def parse_all_day_data(self, all_day_data):
        for i in all_day_data:
            day = all_day_data[i]
            d = StockDay((i, " ", self.symbol), day['1. open'], day['2. high'], day['3. low'], day['4. close'],
                         day['5. adjusted close'], day['6. volume'], day['7. dividend amount'])
            self.historic_data.append(d)
        self.historic_data.reverse()
        return self.historic_data

    def get_historic_high(self):
        print("historic_high:", max(node.close for node in self.historic_data))

    def get_historic_low(self):
        print("historic_low:", min(node.close for node in self.historic_data))

    def is_historic_high(self):
        hh = max(node.close for node in self.historic_data)
        if hh == self.historic_data[0].close:
            return True
        else:
            return False

    def get_supports(self):
        for i, day_data in enumerate(self.historic_data):
            if i < len(self.historic_data)-1 \
                    and day_data.close < self.historic_data[i-1].close \
                    and day_data.close < self.historic_data[i+1].close:
                print(self.historic_data[i-1].close, "<", day_data.close, ">", self.historic_data[i+1].close, "is support")
                stock_day_data = StockDayData()
                stock_day_data.is_support = True
                self.stock_day_data.append(stock_day_data) # TODO hacer solo un append entre sup y res
            print("Day data", day_data.close)

    def get_resistances(self):
        for i, day_data in enumerate(self.historic_data):
            if i < len(self.historic_data)-1 \
                    and day_data.close > self.historic_data[i-1].close \
                    and day_data.close > self.historic_data[i+1].close:
                print(self.historic_data[i-1].close, ">", day_data.close, ">", self.historic_data[i+1].close, "is resistance")
                stock_day_data = StockDayData()
                stock_day_data.is_resistance = True
                self.stock_day_data.append(stock_day_data)  # TODO hacer solo un append entre sup y res
            print("Day data", day_data.close)
