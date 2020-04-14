# Collect interval in seconds
INTERVAL=30

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

DATABASE_URL = 'sqlite:///data.db'


# Plugin configuration


### CPU
# Store statistics per CPU, not only combined
CPU_PER_CPU = True

### Disk
# How often to poll space information, as a number of INTERVALs
DISK_SPACE_FREQUENCY = 10

### Temperatures
# If true, fahrenheit is used, otherwise celsius
TEMPERATURE_USE_FAHRENHEIT = False

### Ping
# Ping hosts
PING_HOSTS = [
    '10.0.0.1',
    '192.168.0.1',
    '1.1.1.1',
    'google.com',
    'bing.com'
]

# How often to send pings, as a number of INTERVALs
PING_FREQUENCY = 10