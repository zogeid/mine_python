from StockConn import *
from StockPlot import *
from offlinedata_StockData import *
from offlinedata_StockData_short import *


class StockController:
    def __init__(self):
        self.conn = None
        self.day_array = None
        self.metadata = None

    def stocks_test_connect(self, input_symbol):
        base_url = 'https://www.alphavantage.co'
        func = 'TIME_SERIES_WEEKLY_ADJUSTED'  # 'TIME_SERIES_INTRADAY'
        # symbol = 'ADS.DE'
        symbol = input_symbol
        datatype = 'json'
        api_key = '2HZ8XGG3MD98X75U'

        self.conn = StockConn(base_url, func, datatype, api_key, symbol)
        self.conn.connect()

        # Retrieve metadata
        self.conn.get_metadata()
        # self.metadata.print()

        # Retrieve all historical data for this Symbol
        all_day_data = self.conn.get_all_day_data()
        self.day_array = self.conn.parse_all_day_data(all_day_data)
        return self.day_array

    def stocks_test_retrieve_data(self):
        self.conn.get_historic_high()
        self.conn.get_historic_low()
        self.conn.get_supports_and_resistances()
        self.conn.print_supports_and_resistances()
        return self.conn

    def stocks_test_plot(self):
        plot(self.day_array)

    def stocks_test(self):
        base_url = 'https://www.alphavantage.co'
        func = 'TIME_SERIES_WEEKLY_ADJUSTED'
        symbol = 'ADS.DE'
        datatype = 'json'
        api_key = '2HZ8XGG3MD98X75U'

        # True data vs. test data set
        datos_de_prueba = True
        if datos_de_prueba:
            print('usando datos de prueba')
            # Establish connection
            self.conn = StockConn()
            all_day_data = stock_data_short
            day_array = self.conn.parse_all_day_data(all_day_data)
        else:
            # Establish connection
            self.conn = StockConn(base_url, func, datatype, api_key, symbol)
            self.conn.connect()

            # Retrieve metadata
            metadata = self.conn.get_metadata()
            metadata.print()

            # Retrieve all historical data for this Symbol
            all_day_data = self.conn.get_all_day_data()
            day_array = self.conn.parse_all_day_data(all_day_data)

        # Retrieve historical high
        self.conn.get_historic_high()

        # Retrieve historical high
        self.conn.get_historic_low()

        # Show if today is an historic high
        if self.conn.is_historic_high():
            print("We have an historic high in", self.conn.historic_data[len(self.conn.historic_data)-1].close)
        else:
            print("Today's", self.conn.historic_data[len(self.conn.historic_data)-1].close, "is not an historic high :(")

        self.conn.get_supports_and_resistances()
        self.conn.print_stock_day_data()

        # Plot retrieved data
        plot(day_array)
