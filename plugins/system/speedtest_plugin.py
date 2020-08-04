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

import json

import logging

class Speedtest(BaseModel):
    time = DateTimeField(index=True, default=datetime.utcnow)
    upload = IntegerField(null=False)
    download = IntegerField(null=False)
    latency = FloatField(null=True)
    jitter = FloatField(null=True)
    packetLoss = IntegerField(null=True)


class SpeedtestPlugin(Plugin):
    models = [Speedtest]

    def get_interval(self):
        return config.SPEEDTEST_INTERVAL

    def execute(self):
        command = ['/usr/local/bin/SpeedTest', '--output', 'json']
        proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = proc.stdout.decode()
        stderr = proc.stderr.decode()

        entry = Speedtest()
        entry.download = 0
        entry.upload = 0

        if proc.returncode == 0:
            try:
                result = json.loads(stdout)
                entry.download = int(float(result['download']))
                entry.upload = int(float(result['upload']))
                entry.latency = float(result['ping'])
                entry.jitter = float(result['jitter'])
            except BaseException as e:
                logging.error(f"SpeedTest failed: {e}")

        else:
            logging.error(f"SpeedTest nonzero return: {proc.returncode}\n-----\n{stdout}\n{stderr}\n\n")
            

        entry.save()
