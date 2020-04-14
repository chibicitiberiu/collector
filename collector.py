import config
import database
import signal
from threading import Event
from plugins.system.cpu_plugin import CpuPlugin
from plugins.system.memory_plugin import MemoryPlugin
from plugins.system.disk_plugin import DiskPlugin
from plugins.system.network_plugin import NetworkPlugin
from plugins.system.temperatures_plugin import TemperaturesPlugin
from plugins.system.ping_plugin import PingPlugin

class Collector(object):

    def __init__(self):
        self.plugins = [
            CpuPlugin(),
            MemoryPlugin(),
            DiskPlugin(),
            NetworkPlugin(),
            TemperaturesPlugin(),
            PingPlugin()
        ]
        self.event = Event()

    def collect_models(self):
        models = []
        for plugin in self.plugins:
            models.extend(plugin.models)
        return models

    def initialize(self):
        models = self.collect_models()
        database.initialize_db()
        database.DB.create_tables(models)

        signal.signal(signal.SIGHUP, self.abort)
        signal.signal(signal.SIGTERM, self.abort)
        signal.signal(signal.SIGINT, self.abort)

    def run(self):
        self.initialize()
        print(f'Started.')

        while not self.event.is_set():
            for plugin in self.plugins:
                # try:
                plugin.execute()
                # except BaseException as ex:
                    # print(ex)
            
            self.event.wait(config.INTERVAL)
            # TODO: calculate wait time based on execution time

        print(f'Stopped.')

    def abort(self, signum, frame):
        print(f'Received signal {signum}, aborting...')
        self.event.set()


if __name__ == "__main__":
    Collector().run()