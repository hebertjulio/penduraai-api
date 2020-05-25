import redis

from django.conf import settings


class Transaction:

    PREFIX = 'transaction'

    db = redis.Redis(
        host=settings.DICTDB_REDIS_HOST,
        port=settings.DICTDB_REDIS_PORT,
        db=settings.DICTDB_REDIS_DB
    )

    code = None
    values = {}

    def __init__(self, code):
        self.code = code

    def __setattr__(self, attr, value):
        if attr in Transaction.__dict__.keys():
            self.__dict__[attr] = value
        else:
            self.values[attr] = value

    def __getattr__(self, attr):
        if attr in Transaction.__dict__.keys():
            return self.__dict__[attr]
        name = ':'.join([self.PREFIX, self.code, attr])
        value = self.db.get(name)
        return value

    def __delattr__(self, attr):
        name = ':'.join([self.PREFIX, self.code, attr])
        self.db.delete(*[name])

    def __del__(self):
        names = [':'.join([self.PREFIX, self.code])]
        self.db.delete(*names)

    @property
    def ttl(self, attr='*'):
        pattern = ':'.join([self.PREFIX, self.code, attr])
        names = self.db.keys(pattern)
        return min(*[self.db.ttl(name) for name in names])

    def exist(self, attr='*'):
        pattern = ':'.join([self.PREFIX, self.code, attr])
        count = len(self.db.keys(pattern))
        return count > 0

    def save(self):
        for attr, value in self.values.items():
            name = ':'.join([self.PREFIX, self.code, attr])
            self.db.set(name, value, ex=60*10)
