from StockConn import *
from StockPlot import *
from StockData import *


class StockController:

    def __init__(self):
        # Establish connection
        self.conn = None
        self.day_array = None

    def stocks_test_connect(self):
        base_url = 'https://www.alphavantage.co'
        func = 'TIME_SERIES_WEEKLY_ADJUSTED'
        symbol = 'ADS.DE'
        datatype = 'json'
        api_key = '2HZ8XGG3MD98X75U'
        print('usando datos de prueba')
        self.conn = StockConn()
        all_day_data = stock_data
        self.day_array = self.conn.parse_all_day_data(all_day_data)

    def stocks_test_retrieve_data(self):
        # Retrieve historical high
        self.conn.get_historic_high()

        # Retrieve historical high
        self.conn.get_historic_low()

        # Show if today is an historic high
        if self.conn.is_historic_high():
            print("We have an historic high in", self.conn.historic_data[len(self.conn.historic_data) - 1].close)
        else:
            print("Today's", self.conn.historic_data[len(self.conn.historic_data) - 1].close, "is not an historic high :(")

        self.conn.get_supports_and_resistances()
        self.conn.print_stock_day_data()

    def stocks_test_plot(self):
        # Plot retrieved data
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
            conn = StockConn()
            all_day_data = stock_data
            day_array = conn.parse_all_day_data(all_day_data)
        else:
            # Establish connection
            conn = StockConn(base_url, func, datatype, api_key, symbol)
            conn.connect()

            # Retrieve metadata
            metadata = conn.get_metadata()
            metadata.print()

            # Retrieve all historical data for this Symbol
            all_day_data = conn.get_all_day_data()
            day_array = conn.parse_all_day_data(all_day_data)

        # Retrieve historical high
        conn.get_historic_high()

        # Retrieve historical high
        conn.get_historic_low()

        # Show if today is an historic high
        if conn.is_historic_high():
            print("We have an historic high in", conn.historic_data[len(conn.historic_data)-1].close)
        else:
            print("Today's", conn.historic_data[len(conn.historic_data)-1].close, "is not an historic high :(")

        conn.get_supports_and_resistances()
        conn.print_stock_day_data()

        # Plot retrieved data
        plot(day_array)
