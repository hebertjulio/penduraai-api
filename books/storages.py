import redis

from django.conf import settings


class Transaction:

    PREFIX_RECORD = 'transaction:record:'
    PREFIX_CHANNEL_NAME = 'transaction:channel_name:'
    EXPIRE_RECORD = 86400  # 1 day to expire
    EXPIRE_CHANNEL_NAME = 86460  # 1 day and 60 seconds to expire

    def __init__(self, key):
        self.storage = redis.Redis(
            host=settings.DICTDB_REDIS_HOST,
            port=settings.DICTDB_REDIS_PORT,
            db=settings.DICTDB_REDIS_DB
        )
        self.key = key

    @property
    def exist(self):
        value = self.storage.exists(
            self.PREFIX_RECORD + self.key,
            self.PREFIX_CHANNEL_NAME + self.key)
        return value == 2

    @property
    def record(self):
        value = self.storage.get(
            self.PREFIX_RECORD + self.key
        )
        return value

    @record.setter
    def record(self, value):
        self.storage.set(
            self.PREFIX_RECORD + self.key,
            value, ex=self.EXPIRE_RECORD
        )

    @record.deleter
    def record(self):
        self.storage.delete(
            self.PREFIX_RECORD + self.key
        )

    @property
    def channel_name(self):
        value = self.storage.get(
            self.PREFIX_CHANNEL_NAME + self.key
        )
        return value

    @channel_name.setter
    def channel_name(self, value):
        self.storage.set(
            self.PREFIX_CHANNEL_NAME + self.key,
            value, ex=self.EXPIRE_CHANNEL_NAME
        )

    @channel_name.deleter
    def channel_name(self):
        self.storage.delete(
            self.PREFIX_CHANNEL_NAME + self.key
        )
