# Collect interval in seconds
DEFAULT_INTERVAL = 30

# Database URL, which defines connection settings.
#
# sqlite:///my_database.db 
#   will create a SqliteDatabase instance for the file my_database.db in the current directory.
#
# sqlite:///:memory:
#   will create an in-memory SqliteDatabase instance.
#
# postgresql://postgres:my_password@localhost:5432/my_database 
#   will create a PostgresqlDatabase instance. A username and password are provided, as well as the host and port to connect to.
#
# mysql://user:passwd@ip:port/my_db 
#   will create a MySQLDatabase instance for the local MySQL database my_db.
#
# mysql+pool://user:passwd@ip:port/my_db?max_connections=20&stale_timeout=300 
#   will create a PooledMySQLDatabase instance for the local MySQL database my_db with max_connections set to 20 and a
#   stale_timeout setting of 300 seconds.

DATABASE_URL = 'postgresql://system_metrics_collector:theMetrixWriteer2123@localhost:5432/system_metrics'


# Plugin configuration


### CPU
CPU_INTERVAL = DEFAULT_INTERVAL
# Store statistics per CPU, not only combined
CPU_PER_CPU = True

### Disk
DISK_USAGE_INTERVAL = DEFAULT_INTERVAL * 10
DISK_IO_INTERVAL = DEFAULT_INTERVAL

### Memory
MEMORY_INTERVAL = DEFAULT_INTERVAL

### Network
NETWORK_INTERVAL = DEFAULT_INTERVAL

### Temperatures
TEMPERATURE_INTERVAL = DEFAULT_INTERVAL

# If true, fahrenheit is used, otherwise celsius
TEMPERATURE_USE_FAHRENHEIT = False

### Ping
# Ping hosts
PING_INTERVAL = 5 * 60              # every 5 min

PING_HOSTS = [
    '10.0.0.1',
    '192.168.0.1',
    '1.1.1.1',
    'google.com',
    'bing.com',
    'tibich.com'
]

### Stocks
STOCKS_INTERVAL = 12 * 60 * 60      # updates daily

STOCKS_TICKERS = {
    'MCRO.L' : 'Micro Focus International PLC',
    '^GSPC' : 'S&P 500',
    '^SPEUP' : 'S&P 350 Europe',
    '^SPG1200' : 'S&P 1200 Global',
    '^IXIC' : 'NASDAQ Composite',
    'BTC-USD' : 'Bitcoin USD',
    'ETH-USD' : 'Ethereum USD',
}

### ROBOR
# Romanian Interbank Offer Rate
ROBOR_INTERVAL = 12 * 60 * 60       # updates daily, every 12 hours should be fine

ROBOR_FIELDS = [
    'ROBOR 6M'
]
