from collections import namedtuple
from datetime import datetime

import psutil
from peewee import *
from playhouse.shortcuts import model_to_dict

import config
from database import BaseModel
from plugins.plugin import Plugin


class DiskUsage(BaseModel):
    time = DateTimeField(index=True, default=datetime.utcnow)
    partition = TextField(null=False)
    mountpoint = TextField(null=False)
    total = BigIntegerField(null=False)
    used = BigIntegerField(null=False)
    free = BigIntegerField(null=False)


class DiskIO(BaseModel):
    time = DateTimeField(index=True, default=datetime.utcnow)
    disk = TextField(null=True)
    read_count = FloatField(null=False)     # all values are per second
    write_count = FloatField(null=False)
    read_speed = FloatField(null=False)
    write_speed = FloatField(null=False)


class DiskUsagePlugin(Plugin):
    models = [DiskUsage]

    def get_interval(self):
        return config.DISK_USAGE_INTERVAL

    def execute(self):
        for partition in psutil.disk_partitions():
            usage = psutil.disk_usage(partition.mountpoint)
            
            entry = DiskUsage()
            entry.partition = partition.device
            entry.mountpoint = partition.mountpoint
            entry.total = usage.total
            entry.used = usage.used
            entry.free = usage.free
            entry.save()


class DiskIOPlugin(Plugin):
    models = [DiskIO]

    def __init__(self):
        self.__previous_io = {}

    def get_interval(self):
        return config.DISK_IO_INTERVAL

    def store_io(self, disk, current):
        previous = self.__previous_io.get(disk, current)

        entry = DiskIO()
        entry.disk = disk
        entry.read_count = (current.read_count - previous.read_count) / self.get_interval()
        entry.write_count = (current.write_count - previous.write_count) / self.get_interval()
        entry.read_speed = (current.read_bytes - previous.read_bytes) / self.get_interval()
        entry.write_speed = (current.write_bytes - previous.write_bytes) / self.get_interval()
        entry.save()

        self.__previous_io[disk] = current

    def execute(self):

        self.store_io(None, psutil.disk_io_counters(perdisk=False))

        io_reads = psutil.disk_io_counters(perdisk=True)
        for disk, current in io_reads.items():
            self.store_io(disk, current)

