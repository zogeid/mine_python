import requests
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
        self.metadata = None
        self.resistances = []
        self.current_resistance = None
        self.supports = []
        self.current_support = None

    def compose_url(self):
        url = self.base_url + '/query?function=' + self.function + '&symbol=' + self.symbol + '&datatype=' + self.datatype + '&apikey=' + self.api_key
        return url

    def connect(self):
        self.stock_request = requests.get(self.url, verify=False)
        if self.stock_request.status_code == 200:
            print("Connection done!")
            # print(self.stock_request.json())

    def get_all_day_data(self):
        result_json = self.stock_request.json()
        return result_json['Weekly Adjusted Time Series']

    def get_metadata(self):
        result_json = self.stock_request.json()
        md = result_json['Meta Data']
        self.metadata = StockMetaData(md['1. Information'], md['2. Symbol'], md['3. Last Refreshed'], md['4. Time Zone'])
        return self.metadata

    def parse_all_day_data(self, all_day_data):
        for i in all_day_data:
            day = all_day_data[i]
            d = StockDay(i, day['1. open'], day['2. high'], day['3. low'], day['4. close'],
                         day['5. adjusted close'], day['6. volume'], day['7. dividend amount'])
            self.historic_data.append(d)
        self.historic_data.reverse()
        return self.historic_data

    def get_historic_high(self):
        return max(node.close for node in self.historic_data)

    def get_historic_high_day(self):
        historic_high_day = self.historic_data[0]
        for node in self.historic_data:
            if node.high > historic_high_day.high:
                historic_high_day = node
        return historic_high_day

    def get_historic_high_day_to_date(self, day_data):
        historic_high_day = self.historic_data[0]
        index_to = self.historic_data.index(day_data)
        for node in self.historic_data[:index_to+1]:
            if node.high > historic_high_day.high:
                historic_high_day = node
        return historic_high_day

    def get_historic_low(self):
        return min(node.close for node in self.historic_data)

    def is_historic_high(self):
        hh = max(node.close for node in self.historic_data)
        if hh == self.historic_data[0].close:
            return True
        else:
            return False

    def set_resistance(self, day_data):
        self.resistances.append(day_data)
        self.current_resistance = day_data

    def set_support(self, day_data):
        self.supports.append(day_data)
        self.current_support = day_data

    def print_supports_and_resistances(self):
        print("Current resistance: ")
        self.current_resistance.print()
        print("Current support: ")
        self.current_support.print()

    def get_supports_and_resistances(self):
        # sdd = StockDayData(day_data)
        turn_resistance = True
        for i, day_data in enumerate(self.historic_data):
            # Primera iteración
            # Resistencia: se produce cuando la minima < minima inmediatamente anterior.
            # Vale lo que vale el max. historico hasta ese momento
            if turn_resistance:
                if 0 < i < len(self.historic_data) - 1 and day_data.low < self.historic_data[i - 1].low:  # min < min
                    # Si no hay ninguna resistencia, coge el max. historico hasta ese momento
                    if len(self.resistances) == 0:
                        # coger el máximo histórico hasta ese momento
                        self.set_resistance(self.get_historic_high_day_to_date(day_data))
                        turn_resistance = False

                    # Tenemos resistencias calculadas previamente
                    else:
                        # Si es mayor a la resistencia actual, la ñadimos como nueva resistencia
                        if day_data.high > self.current_resistance.high:
                            self.set_resistance(day_data)
                            turn_resistance = False

            # Soporte: se produce cuando se rompe la resistencia
            # Es el minimo comprendido entre el punto A (resistencia previa) y su ruptura(=resistencia) ahora.
            elif not turn_resistance:
                if len(self.resistances) == 1:  # Si tenemos 1 resistencias miramos desde el día 0
                    prev_resistance = self.historic_data[0]
                    current_low = prev_resistance

                    for hd in self.historic_data:
                        if hd.date >= prev_resistance.date:
                            if hd.low < current_low.low:
                                current_low = hd

                else:  # Tiene que haber al menos 2: la recien rota y la del previo if
                    prev_resistance = self.resistances[-2]
                    current_low = prev_resistance

                    for hd in self.historic_data:
                        if hd.date >= prev_resistance.date:
                            if hd.low < current_low.low:
                                current_low = hd

                turn_resistance = True
                self.set_support(current_low)

    def print_stock_day_data(self):
        for s in self.stock_day_data:
            s.print()
