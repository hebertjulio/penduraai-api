import redis
import json
import uuid

from django.utils.translation import gettext_lazy as _
from django.conf import settings

from model_utils import Choices

from .services import generate_signature


class Transaction:

    STATUS = Choices(
        ('awaiting', _('awaiting')),
        ('accepted', _('accepted')),
        ('rejected', _('rejected')),
    )

    PREFIX = 'transaction'

    __DEFAULT_DATA = {
        'payload': {}, 'status': STATUS.awaiting
    }

    def __init__(self, _id=str(uuid.uuid4())):
        self.__db = redis.Redis(**settings.REDIS_CONFIG)
        self.__name = ':'.join([self.PREFIX, _id])
        if not self.exist():
            self.__set_data(self.__DEFAULT_DATA)

    @property
    def id(self):
        value = self.__name.split(':')[1]
        return value

    @id.setter
    def id(self, value):
        raise NotImplementedError

    @id.deleter
    def id(self):
        raise NotImplementedError

    @property
    def payload(self):
        data = self.__get_data()
        value = data['payload']
        return value

    @payload.setter
    def payload(self, value):
        if not isinstance(value, dict):
            raise ValueError
        data = self.__get_data()
        data['payload'] = value
        self.__set_data(data)

    @payload.deleter
    def payload(self):
        raise NotImplementedError

    @property
    def status(self):
        data = self.__get_data()
        value = data['status']
        return value

    @status.setter
    def status(self, value):
        if value not in self.STATUS:
            raise ValueError
        data = self.__get_data()
        data['status'] = value
        self.__set_data(data)

    @status.deleter
    def status(self):
        raise NotImplementedError

    @property
    def ttl(self):
        value = self.__db.ttl(self.__name)
        return value

    @ttl.setter
    def ttl(self, _):
        raise NotImplementedError

    @ttl.deleter
    def ttl(self):
        raise NotImplementedError

    @property
    def expire(self):
        raise NotImplementedError

    @expire.setter
    def expire(self, value):
        if not isinstance(value, int):
            raise ValueError
        self.__db.expire(self.__name, value)

    @expire.deleter
    def expire(self):
        raise NotImplementedError

    @property
    def signature(self):
        value = generate_signature(self.__payload)
        return value

    @signature.setter
    def signature(self, _):
        raise NotImplementedError

    @signature.deleter
    def signature(self):
        raise NotImplementedError

    def exist(self):
        keys = self.__db.keys(self.__name)
        count = len(keys)
        return count == 1

    def __get_data(self):
        value = self.__db.get(self.__name)
        if value is None:
            return self.__DEFAULT_DATA
        value = json.loads(value)
        return value

    def __set_data(self, value):
        if not isinstance(value, dict):
            raise ValueError
        value = json.dumps(value)
        expire = self.ttl if self.exist() else 60
        self.__db.set(self.__name, value, ex=expire)

    def delete(self):
        self.__db.delete(*[self.__name])

    def __str__(self):
        return self.__name

    def __repr__(self):
        value = json.dumps(self.__get_data())
        return '%s %s' % (self.__name, value)
