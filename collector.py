import config
import database
import signal
from apscheduler.schedulers.blocking import BlockingScheduler
from threading import Event
from plugins.system.cpu_plugin import CpuPlugin
from plugins.system.memory_plugin import MemoryPlugin
from plugins.system.disk_plugin import DiskIOPlugin, DiskUsagePlugin
from plugins.system.network_plugin import NetworkPlugin
from plugins.system.temperatures_plugin import TemperaturesPlugin
from plugins.system.ping_plugin import PingPlugin
from plugins.finance.stocks_plugin import StocksPlugin
from plugins.finance.robor_plugin import RoborPlugin
import logging


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
        for plugin in self.plugins:
            self.scheduler.add_job(plugin.execute, 'interval', seconds=plugin.get_interval())

    def run(self):
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.INFO)

        models = self.collect_models()
        database.initialize_db()
        database.DB.create_tables(models)

        self.schedule_plugins()
        # signal.signal(signal.SIGHUP, self.abort)
        # signal.signal(signal.SIGTERM, self.abort)
        # signal.signal(signal.SIGINT, self.abort)
        print(f'Started.')

        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass

        print(f'Stopped.')

    def abort(self, signum, frame):
        print(f'Received signal {signum}, aborting...')
        self.event.set()


if __name__ == "__main__":
    Collector().run()