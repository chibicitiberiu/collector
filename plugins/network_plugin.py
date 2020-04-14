from collections import namedtuple
from datetime import datetime

import psutil
from peewee import *
from playhouse.shortcuts import model_to_dict

import config
from database import BaseModel

from .plugin import Plugin


class NetworkIO(BaseModel):
    time = DateTimeField(index=True, default=datetime.now)
    nic = TextField(null=True)
    packets_sent = FloatField(null=False)     # all values are per second
    packets_recv = FloatField(null=False)
    bytes_sent = FloatField(null=False)
    bytes_recv = FloatField(null=False)


class NetworkPlugin(Plugin):
    models = [NetworkIO]

    def __init__(self):
        self.__previous_io = {}

    def store_io(self, nic, current):
        previous = self.__previous_io.get(nic, current)

        entry = NetworkIO()
        entry.nic = nic
        entry.packets_sent = (current.packets_sent - previous.packets_sent) / config.INTERVAL
        entry.packets_recv = (current.packets_recv - previous.packets_recv) / config.INTERVAL
        entry.bytes_sent = (current.bytes_sent - previous.bytes_sent) / config.INTERVAL
        entry.bytes_recv = (current.bytes_recv - previous.bytes_recv) / config.INTERVAL
        entry.save()

        self.__previous_io[nic] = current

    def execute(self):

        self.store_io(None, psutil.net_io_counters(pernic=False))

        io_reads = psutil.net_io_counters(pernic=True)
        for nic, current in io_reads.items():
            self.store_io(nic, current)