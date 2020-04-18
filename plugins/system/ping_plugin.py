import subprocess
import re
import subprocess
from datetime import datetime

import psutil
from peewee import *
from playhouse.shortcuts import model_to_dict

import config
from database import BaseModel
from plugins.plugin import Plugin


class Ping(BaseModel):
    time = DateTimeField(index=True, default=datetime.utcnow)
    host = TextField(null=False)
    ping = FloatField(null=True) # null = timeout or error


class PingPlugin(Plugin):
    models = [Ping]

    def __init__(self):
        self.__timeout = 20

    def get_interval(self):
        return config.PING_INTERVAL

    def do_ping(self, host):
        command = ['ping', '-c', '1', '-W', str(self.__timeout), host]
        proc = subprocess.run(command, stdout=subprocess.PIPE)
        stdout = proc.stdout.decode()

        entry = Ping()
        entry.host = host
        entry.ping = None

        match = re.search(r'time=([\d\.]+) ms', stdout)
        if match is not None:
            entry.ping = float(match.group(1))

        entry.save()

    def execute(self):
        for host in config.PING_HOSTS:
            self.do_ping(host)
