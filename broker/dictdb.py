import redis
import json
import uuid

from django.conf import settings

from .services import generate_signature


class Transaction:

    __PREFIX = 'transaction'

    def __init__(self, _uuid=str(uuid.uuid4())):
        self.__db = redis.Redis(
            host=settings.DICTDB_REDIS_HOST,
            port=settings.DICTDB_REDIS_PORT,
            db=settings.DICTDB_REDIS_DB
        )
        self.__uuid = _uuid

    @property
    def name(self):
        return ':'.join([self.__PREFIX, self.uuid])

    @name.setter
    def name(self, _):
        raise NotImplementedError

    @name.deleter
    def name(self):
        raise NotImplementedError

    @property
    def data(self):
        data = self.__db.get(self.name) or '{}'
        data = json.loads(data)
        return data

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError
        value = json.dumps(value)
        ex = self.ttl if self.ttl > 0 else 60*2
        self.__db.set(self.name, value, ex=ex)

    @data.deleter
    def data(self):
        raise NotImplementedError

    @property
    def uuid(self):
        return self.__uuid

    @uuid.setter
    def uuid(self, value):
        raise NotImplementedError

    @uuid.deleter
    def uuid(self):
        raise NotImplementedError

    @property
    def expire(self):
        raise NotImplementedError

    @expire.setter
    def expire(self, value):
        self.__db.expire(self.name, value)

    @expire.deleter
    def expire(self, value):
        raise NotImplementedError

    @property
    def ttl(self):
        return self.__db.ttl(self.name)

    @ttl.setter
    def ttl(self, _):
        raise NotImplementedError

    @ttl.deleter
    def ttl(self):
        raise NotImplementedError

    @property
    def signature(self):
        signature = generate_signature(self.uuid, self.data)
        return signature

    @signature.setter
    def signature(self, _):
        raise NotImplementedError

    @signature.deleter
    def signature(self):
        raise NotImplementedError

    def exist(self):
        keys = self.__db.keys(self.name)
        count = len(keys)
        return count == 1

    def delete(self):
        self.__db.delete(*[self.name])

    def __str__(self):
        data = json.dumps(self.data)
        return '%s %s' % (self.name, data)

    def __repr__(self):
        data = json.dumps(self.data)
        return '%s %s' % (self.name, data)
