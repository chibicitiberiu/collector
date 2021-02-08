from datetime import datetime, timedelta

import psutil
from peewee import *

import config
from database import BaseModel
from plugins.plugin import Plugin


class Memory(BaseModel):
    time = DateTimeField(index=True, default=datetime.utcnow)
    total = BigIntegerField(null=False)
    available = BigIntegerField(null=False)
    used = BigIntegerField(null=False)
    free = BigIntegerField(null=False)
    active = BigIntegerField(null=True)
    inactive = BigIntegerField(null=True)
    buffers = BigIntegerField(null=True)
    cached = BigIntegerField(null=True)
    swap_total = BigIntegerField(null=False)
    swap_used = BigIntegerField(null=False)
    swap_free = BigIntegerField(null=False)


class MemoryPlugin(Plugin):
    models = [Memory]

    def get_interval(self):
        return config.MEMORY_INTERVAL

    def execute(self):
        vmem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        entry = Memory()
        entry.total = vmem.total
        entry.available = vmem.available
        entry.used = vmem.used
        entry.free = vmem.free
        entry.active = getattr(vmem, 'active', None)
        entry.inactive = getattr(vmem, 'inactive', None)
        entry.buffers = getattr(vmem, 'buffers', None)
        entry.cached = getattr(vmem, 'cached', None)
        entry.swap_total = swap.total
        entry.swap_free = swap.free
        entry.swap_used = swap.used
        entry.save()

    def cleanup(self):
        limit = datetime.utcnow() - timedelta(days=config.MEMORY_RETAIN_DAYS)
        return Memory.delete().where(Memory.time < limit).execute()
