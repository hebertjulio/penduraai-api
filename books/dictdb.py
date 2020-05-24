from abc import ABC
from redis import Redis

from django.conf import settings


class Storage(ABC):

    PREFIX = 'storage'

    def __init__(self, key):
        host = settings.DICTDB_REDIS_HOST
        port = settings.DICTDB_REDIS_PORT
        db = settings.DICTDB_REDIS_DB
        self.db = Redis(host=host, port=port, db=db)
        self.key = key

    def __setitem__(self, key, value):
        self.db.set(
            ':'.join([self.PREFIX, self.key, key]), value
        )

    def __getitem__(self, key):
        return self.db.get(
            ':'.join([self.PREFIX, self.key, key])
        )

    def __delitem__(self, key):
        self.db.delete(
            ':'.join([self.PREFIX, self.key, key])
        )

    def __len__(self):
        return len(self.key())

    def __delattr__(self, instance):
        self.db.delete(*self.keys())

    def keys(self):
        return self.db.keys(
            ':'.join([self.PREFIX, self.key, '*'])
        )
