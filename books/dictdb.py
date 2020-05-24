from abc import ABC
from redis import Redis

from django.conf import settings


class Storage(ABC):

    PREFIX = 'storage'

    def __init__(self, uuid):
        host = settings.DICTDB_REDIS_HOST
        port = settings.DICTDB_REDIS_PORT
        db = settings.DICTDB_REDIS_DB
        self.db = Redis(host=host, port=port, db=db)
        self.uuid = uuid

    def __setitem__(self, key, value):
        name = ':'.join([self.PREFIX, self.uuid, key])
        self.db.set(name, value)

    def __getitem__(self, key):
        name = ':'.join([self.PREFIX, self.uuid, key])
        value = self.db.get(name)
        return value

    def __delitem__(self, key):
        name = ':'.join([self.PREFIX, self.uuid, key])
        self.db.delete(name)

    def __len__(self):
        name = ':'.join([self.PREFIX, self.uuid, '*'])
        names = self.db.keys(name)
        count = len(names)
        return count

    def __contains__(self, key):
        names = ':'.join([self.PREFIX, self.uuid, key])
        count = self.db.exists(*names)
        return count == 1

    def __delattr__(self, instance):
        patterns = ':'.join([self.PREFIX, self.uuid, '*'])
        names = self.db.keys(patterns)
        self.db.delete(*names)
