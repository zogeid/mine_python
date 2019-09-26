from StockConn import *
from StockPlot import *
from StockData import *

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

# Plot retrieved data
plot(day_array)
