from datetime import datetime, timedelta

import psutil
from peewee import *
from playhouse.shortcuts import model_to_dict

import config
from database import BaseModel
from plugins.plugin import Plugin


class Cpu(BaseModel):
    time = DateTimeField(index=True, default=datetime.utcnow)
    cpu = SmallIntegerField(null=True)
    idle_pct = FloatField(null=False)
    user_pct = FloatField(null=False)
    system_pct = FloatField(null=False)
    nice_pct = FloatField(null=True)
    iowait_pct = FloatField(null=True)
    irq_pct = FloatField(null=True)
    softirq_pct = FloatField(null=True)
    freq_min = FloatField(null=True)
    freq_current = FloatField(null=True)
    freq_max = FloatField(null=True)


class CpuPlugin(Plugin):
    models = [Cpu]

    def get_interval(self):
        return config.CPU_INTERVAL

    def store(self, cpu, times, freq):
        entry = Cpu()
        entry.cpu = cpu
        entry.idle_pct = times.idle
        entry.user_pct = times.user
        entry.system_pct = times.system
        entry.nice_pct = getattr(times, 'nice', None)
        entry.iowait_pct = getattr(times, 'iowait', None)
        entry.irq_pct = getattr(times, 'irq', getattr(times, 'interrupt', None))
        entry.softirq_pct = getattr(times, 'softirq', None)
        entry.freq_min = getattr(freq, 'min', None)
        entry.freq_current = getattr(freq, 'current', None)
        entry.freq_max = getattr(freq, 'max', None)
        entry.save()

    def execute(self):
        self.store(None, psutil.cpu_times_percent(percpu=False), psutil.cpu_freq(percpu=False))

        if config.CPU_PER_CPU:
            times = psutil.cpu_times_percent(percpu=True)
            freqs = psutil.cpu_freq(percpu=True)
            for i in range(len(times)):
                self.store(i, times[i], freqs[i])

    def cleanup(self):
        limit = datetime.utcnow() - timedelta(days=config.CPU_RETAIN_DAYS)
        return Cpu.delete().where(Cpu.time < limit).execute()