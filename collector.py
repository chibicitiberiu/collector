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
from plugins.system.speedtest_plugin import SpeedtestPlugin


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
            SpeedtestPlugin(),

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
            self.scheduler.add_job(plugin.execute_wrapper, 'interval', 
                                   seconds=plugin.get_interval(),
                                   start_date=start_date,
                                   name=plugin.__class__.__name__)

    def schedule_cleanup(self):
        start_date = datetime.now() + timedelta(seconds=100)
        self.scheduler.add_job(self.cleanup, 'interval', 
                               hours=24,
                               start_date=start_date,
                               name='Cleanup')

    def run(self):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)
        logging.getLogger('apscheduler').setLevel(logging.INFO)

        models = self.collect_models()
        database.initialize_db()
        with database.DB.connection_context():
            database.DB.create_tables(models)

        self.schedule_plugins()
        self.schedule_cleanup()
        logging.info('Started.')

        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass

        logging.info(f'Stopped.')

    def cleanup(self):
        for plugin in self.plugins:
            logging.info(f'Cleaning up {plugin.__class__.__name__}...')
            try:
                items = plugin.cleanup_wrapper()
                logging.info(f'... deleted {items} entries')
            except BaseException as e:
                logging.error("Cleanup error:", exc_info=e)
                pass

if __name__ == "__main__":
    try:
        Collector().run()
    except BaseException as ex:
        logging.critical("Unhandled exception.", exc_info=ex)
