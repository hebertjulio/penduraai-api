import redis

from django.conf import settings


class Transaction:

    PREFIX = 'transaction'

    db = redis.Redis(
        host=settings.DICTDB_REDIS_HOST,
        port=settings.DICTDB_REDIS_PORT,
        db=settings.DICTDB_REDIS_DB
    )

    def __init__(self, key):
        self.key = key

    @property
    def channel_name(self):
        name = ':'.join([self.PREFIX, self.key, 'channel_name'])
        value = self.db.get(name)
        return value

    @channel_name.setter
    def channel_name(self, value):
        name = ':'.join([self.PREFIX, self.key, 'channel_name'])
        self.db.set(name, value, ex=60*10)  # 10 minutes

    @property
    def data(self):
        name = ':'.join([self.PREFIX, self.key, 'data'])
        value = self.db.get(name)
        return value

    @data.setter
    def data(self, value):
        name = ':'.join([self.PREFIX, self.key, 'data'])
        self.db.set(name, value, ex=60*10)  # 10 minutes

    @property
    def ttl(self):
        pattern = ':'.join([self.PREFIX, self.key, '*'])
        names = self.db.keys(pattern)
        return min(*[self.db.ttl(name) for name in names])

    def exist(self):
        pattern = ':'.join([self.PREFIX, self.key, '*'])
        count = len(self.db.keys(pattern))
        return count == 2

    def __del__(self):
        names = [':'.join([self.PREFIX, self.key])]
        self.db.delete(*names)
