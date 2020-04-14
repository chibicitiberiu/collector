from collections import namedtuple
from datetime import datetime

import psutil
from peewee import *
from playhouse.shortcuts import model_to_dict

import config
from database import BaseModel
from plugins.plugin import Plugin


class Temperatures(BaseModel):
    time = DateTimeField(index=True, default=datetime.now)
    sensor = TextField(null=False)
    sensor_label = TextField(null=False)
    current = FloatField(null=False)     # all values are per second
    high = FloatField(null=False)
    critical = FloatField(null=False)


class TemperaturesPlugin(Plugin):
    models = [Temperatures]

    def execute(self):
        for sensor, temps in psutil.sensors_temperatures(config.TEMPERATURE_USE_FAHRENHEIT).items():
            for temp in temps:
                entry = Temperatures()
                entry.sensor = sensor
                entry.sensor_label = temp.label
                entry.current = temp.current
                entry.high = temp.high
                entry.critical = temp.critical
                entry.save()
