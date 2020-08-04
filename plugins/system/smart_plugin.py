from datetime import datetime

import psutil
from peewee import *
from playhouse.shortcuts import model_to_dict

import config
from database import BaseModel
from plugins.plugin import Plugin


class SMART(BaseModel):
    time = DateTimeField(index=True, default=datetime.utcnow)
    drive = TextField(null=False)
    attribute_id = IntegerField(null=False)
    attribute_name = TextField(null=False)
    value = IntegerField(null=False)
    worst = IntegerField(null=False)
    threshold = IntegerField(null=False)
    raw = IntegerField(null=False)


class SMARTPlugin(Plugin):
    models = [SMART]

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
