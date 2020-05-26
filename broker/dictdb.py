import redis
import uuid

from django.conf import settings


class Transaction:

    PREFIX = 'transaction'

    db = redis.Redis(
        host=settings.DICTDB_REDIS_HOST,
        port=settings.DICTDB_REDIS_PORT,
        db=settings.DICTDB_REDIS_DB
    )

    def __init__(self, code=str(uuid.uuid4()), expire=60*10):
        self.code = code
        self.expire = expire

    @property
    def data(self):
        name = ':'.join([self.PREFIX, self.code])
        data = self.db.get(name)
        return data

    @data.setter
    def data(self, data):
        name = ':'.join([self.PREFIX, self.code])
        self.db.set(name, data, ex=self.expire)

    @data.deleter
    def data(self):
        raise NotImplementedError

    @property
    def ttl(self):
        name = ':'.join([self.PREFIX, self.code])
        return self.db.ttl(name)

    @ttl.setter
    def ttl(self, expire):
        name = ':'.join([self.PREFIX, self.code])
        self.db.expire(name, expire)

    @ttl.deleter
    def ttl(self):
        raise NotImplementedError

    @property
    def code(self):
        return self.code

    @code.setter
    def code(self, _):
        raise NotImplementedError

    @code.deleter
    def code(self):
        raise NotImplementedError

    def exist(self):
        pattern = ':'.join([self.PREFIX, self.code])
        count = len(self.db.keys(pattern))
        return count == 1

    def __del__(self):
        names = [':'.join([self.PREFIX, self.code])]
        self.db.delete(*names)
