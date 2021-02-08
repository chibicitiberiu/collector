# Tibi Collector

A really lightweight and easy to configure alternative to collectd.

## Motivation

I wanted a simple solution of monitoring my Linux server, and the existing solutions were way too complex for my needs. So I decided to write my own tool, which simply polls the system resources at a fixed interval. It is flexible enough so it can be made to monitor pretty much anything, as the finance plugins demonstrate.

## Setup

### 1. Clone this repository

~~~sh
git clone https://github.com/chibicitiberiu/collector.git
~~~

### 2. Install the dependencies

~~~sh
sudo apt install python3 python3-pip
sudo pip3 install -r requirements.txt
~~~

Some plugins have additional dependencies:

* speedtest plugin: depends on https://github.com/taganaka/SpeedTest to be built and installed
* SMART plugin: `sudo apt install smartmontools`

For the database, you will need to install and setup your preferred database and also install the proper python3 drivers:

* Postgres: psycopg2
* MySQL: MySQLdb
* MySQL: pymysql
* SQLite: sqlite3
* CockroachDB: see psycopg2

Check the Peewee documentation for more details about supported databases and advanced connection URLs.

### 3. Configure

The configuration options can be found in the `config.py` file. Most options are self explanatory, and there are comments explaining how to setup the more complicated ones.

To completely disable a plugin, just comment it in the `collector.py` file. For example, to disable the ROBOR plugin, comment it like this:

~~~python
def __init__(self):
    self.plugins = [
        .......
        # finance
        StocksPlugin(),
        #RoborPlugin()
    ]
    .....
~~~

### 4. Install

```
sudo ./install.sh
```

The `install.sh` script sets up a systemd service called `tcollector`. You will be able to control the service using the `systemctl` command.

If something isn't working properly, you can check the logs using the journalctl command:

```
journalctl -n 1000 _SYSTEMD_UNIT=tcollector.service
```

## Development

All PRs are welcome.
