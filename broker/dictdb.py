import redis
import json
import uuid

from django.conf import settings

from .services import generate_signature


class Transaction:

    __REDIS_CONFIG = {
        'host': settings.DICTDB_REDIS_HOST,
        'port': settings.DICTDB_REDIS_PORT,
        'db': settings.DICTDB_REDIS_DB
    }

    __PREFIX = 'transaction'

    __DEFAULT_DATA = '''{
        "payload": {},
        "status": "waiting"
    }'''

    def __init__(self, _id=str(uuid.uuid4())):
        self.__db = redis.Redis(**self.__REDIS_CONFIG)
        self.__id = _id
        self.__data = self.__db.get(self.name) or self.__DEFAULT_DATA
        self.__data = json.loads(self.__data)

    @property
    def name(self):
        return ':'.join([self.__PREFIX, self.id])

    @name.setter
    def name(self, _):
        raise NotImplementedError

    @name.deleter
    def name(self):
        raise NotImplementedError

    @property
    def payload(self):
        value = self.__data['payload']
        return value

    @payload.setter
    def payload(self, value):
        self.__data['payload'] = value

    @payload.deleter
    def payload(self):
        raise NotImplementedError

    @property
    def status(self):
        value = self.__data['status']
        return value

    @status.setter
    def status(self, value):
        self.__data['status'] = value

    @status.deleter
    def status(self):
        raise NotImplementedError

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise NotImplementedError

    @id.deleter
    def id(self):
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
        signature = generate_signature(self.id, self.payload)
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

    def save(self, expire=60*2):
        value = json.dumps(self.__data)
        ex = self.ttl if self.ttl > 0 else expire
        self.__db.set(self.name, value, ex=ex)

    def delete(self):
        self.__db.delete(*[self.name])

    def __str__(self):
        value = json.dumps(self.__data)
        return '%s %s' % (self.name, value)

    def __repr__(self):
        value = json.dumps(self.__data)
        return '%s %s' % (self.name, value)
