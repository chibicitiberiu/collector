from collections import namedtuple
from datetime import datetime

import psutil
from peewee import *
from playhouse.shortcuts import model_to_dict

import config
from database import BaseModel
from plugins.plugin import Plugin


class NetworkIO(BaseModel):
    time = DateTimeField(index=True, default=datetime.utcnow)
    nic = TextField(null=True)
    packets_sent = FloatField(null=False)     # all values are per second
    packets_recv = FloatField(null=False)
    bytes_sent = FloatField(null=False)
    bytes_recv = FloatField(null=False)


class NetworkPlugin(Plugin):
    models = [NetworkIO]

    def __init__(self):
        self.__previous_io = {}

    def get_interval(self):
        return config.NETWORK_INTERVAL

    def store_io(self, nic, current):
        previous = self.__previous_io.get(nic, current)

        entry = NetworkIO()
        entry.nic = nic
        entry.packets_sent = (current.packets_sent - previous.packets_sent) / self.get_interval()
        entry.packets_recv = (current.packets_recv - previous.packets_recv) / self.get_interval()
        entry.bytes_sent = (current.bytes_sent - previous.bytes_sent) / self.get_interval()
        entry.bytes_recv = (current.bytes_recv - previous.bytes_recv) / self.get_interval()
        entry.save()

        self.__previous_io[nic] = current

    def execute(self):

        self.store_io(None, psutil.net_io_counters(pernic=False))

        io_reads = psutil.net_io_counters(pernic=True)
        for nic, current in io_reads.items():
            self.store_io(nic, current)
