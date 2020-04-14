import asyncio
import re
import subprocess
from datetime import datetime

import psutil
from peewee import *
from playhouse.shortcuts import model_to_dict

import config
from database import BaseModel

from .plugin import Plugin


class Ping(BaseModel):
    time = DateTimeField(index=True, default=datetime.now)
    host = TextField(null=False)
    ping = FloatField(null=True) # null = timeout or error


class PingPlugin(Plugin):
    models = [Ping]

    def __init__(self):
        self.__timeout = config.INTERVAL // 3
        self.__i = 0

    async def do_ping(self, host):
        command = ['ping', '-c', '1', '-W', str(self.__timeout), host]
        proc = await asyncio.create_subprocess_shell(' '.join(command), 
                                                     stdout=asyncio.subprocess.PIPE)

        stdout,_ = await proc.communicate()
        stdout = stdout.decode()

        entry = Ping()
        entry.host = host
        entry.ping = None

        match = re.search(r'time=([\d\.]+) ms', stdout)
        if match is not None:
            entry.ping = float(match.group(1))

        entry.save()
        print(model_to_dict(entry))

    async def execute_internal(self):
        await asyncio.gather(*[self.do_ping(host) for host in config.PING_HOSTS])

    def execute(self):
        if (self.__i % config.PING_FREQUENCY) == 0:
            if getattr(asyncio, 'run', None) is not None:
                # Python 3.7+
                asyncio.run(self.execute_internal())
            else:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.execute_internal())
                loop.close()
        
        self.__i += 1
