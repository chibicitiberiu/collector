import logging
import signal
from datetime import datetime, timedelta
from threading import Event

from apscheduler.schedulers.blocking import BlockingScheduler

import config
import database
from plugins.finance.robor_plugin import RoborPlugin
from plugins.finance.stocks_plugin import StocksPlugin
from plugins.system.cpu_plugin import CpuPlugin
from plugins.system.disk_plugin import DiskIOPlugin, DiskUsagePlugin
from plugins.system.memory_plugin import MemoryPlugin
from plugins.system.network_plugin import NetworkPlugin
from plugins.system.ping_plugin import PingPlugin
from plugins.system.temperatures_plugin import TemperaturesPlugin


class Collector(object):

    def __init__(self):
        self.plugins = [
            # system
            CpuPlugin(),
            MemoryPlugin(),
            DiskUsagePlugin(),
            DiskIOPlugin(),
            NetworkPlugin(),
            TemperaturesPlugin(),
            PingPlugin(),

            # finance
            StocksPlugin(),
            RoborPlugin()
        ]
        self.event = Event()
        self.scheduler = BlockingScheduler()

    def collect_models(self):
        models = []
        for plugin in self.plugins:
            models.extend(plugin.models)
        return models

    def schedule_plugins(self):
        start_date = datetime.now() + timedelta(seconds=10)
        for plugin in self.plugins:
            self.scheduler.add_job(plugin.execute, 'interval', 
                                   seconds=plugin.get_interval(),
                                   start_date=start_date)

    def run(self):
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.INFO)

        models = self.collect_models()
        database.initialize_db()
        database.DB.create_tables(models)

        self.schedule_plugins()
        logging.info('Started.')

        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass

        logging.info(f'Stopped.')


if __name__ == "__main__":
    try:
        Collector().run()
    except BaseException as ex:
        logging.critical("Unhandled exception.", exc_info=ex)
