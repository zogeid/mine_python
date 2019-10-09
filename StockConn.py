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
        self.set_support(day_data)

    def is_resistance(self, day_data):
        # Resistencia: se produce cuando la minima < minima inmediatamente anterior.
        # Vale lo que vale el max. historico hasta ese momento
        # 	solo se pone stop cuando hay resistencia
        # 	cuando, con resistencia puesta, se rompe el max historico, se compra
        # 	resistencia es el trigger para poner el stop

        # Si no hay ninguna resistencia, es el primer valor, lo hacemos resistencia
        if len(self.resistances) == 0:
            self.set_resistance(day_data)
            return True
        else:
            # Es mayor a la resistencia actual, tenemos nueva resistencia, la actualizamos y la añadimos
            if day_data.high > self.current_resistance.high:
                self.set_resistance(day_data)
                return True
        return False

    def is_support(self, day_data):
        # Soporte: se produce cuando se rompe la resistencai.
        # Es el minimo comprenddido entre el punto A (resistencia previa) y su ruptura(=resistencia) ahora.
        # Si no hay ningun soporte, es el primer valor, lo hacemos soporte
        if len(self.supports) == 0:
            self.set_support(day_data)
            return True
        else:
            # TODO no tengo clara la definicion
            if day_data.high > self.current_resistance.high:
                self.set_resistance(day_data)
                return True
        return False

    def get_supports_and_resistances(self):
        turn_resistance = True
        for i, day_data in enumerate(self.historic_data):
            sdd = StockDayData(day_data)
            if turn_resistance and self.is_resistance(day_data):
                sdd.is_resistance = True
                turn_resistance = False
            elif not turn_resistance and self.is_support(day_data):
                sdd.is_support = True
                turn_resistance = True

            self.stock_day_data.append(sdd)

    def print_stock_day_data(self):
        for s in self.stock_day_data:
            s.print()
