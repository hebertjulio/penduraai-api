import redis
import json

from django.utils.translation import gettext_lazy as _
from django.conf import settings

from model_utils import Choices

from .services import generate_signature


class Transaction:

    ACTION = Choices(
        ('new_record', _('new record')),
        ('new_customer_record', _('new customer record')),
    )

    STATUS = Choices(
        ('no_exist', _('no exist')),
        ('awaiting', _('awaiting')),
        ('accepted', _('accepted')),
        ('rejected', _('rejected')),
    )

    PREFIX = 'transaction'

    __DEFAULT_DATA = '''{
        "payload": {}, "status": "%s"
    }'''

    def __init__(self, _id):
        self.__db = redis.Redis(**settings.TRANSACTION_REDIS_CONFIG)
        self.__name = ':'.join([self.PREFIX, _id])
        data = self.__db.get(self.__name)
        data = data or self.__DEFAULT_DATA % Transaction.STATUS.no_exist
        self.__data = json.loads(data)

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
    def action(self):
        value = self.__data['action']
        return value

    @action.setter
    def action(self, value):
        if value not in self.ACTION:
            raise ValueError
        self.__data['action'] = value

    @action.deleter
    def action(self):
        raise NotImplementedError

    @property
    def payload(self):
        value = self.__data['payload']
        return value

    @payload.setter
    def payload(self, value):
        if not isinstance(value, dict):
            raise ValueError
        self.__data['payload'] = value

    @payload.deleter
    def payload(self):
        raise NotImplementedError

    @property
    def creditor(self):
        value = self.__data['creditor']
        return value

    @creditor.setter
    def creditor(self, value):
        if not isinstance(value, int):
            raise ValueError
        self.__data['creditor'] = value

    @creditor.deleter
    def creditor(self):
        raise NotImplementedError

    @property
    def status(self):
        value = self.__data['status']
        return value

    @status.setter
    def status(self, value):
        if value not in self.STATUS:
            raise ValueError
        self.__data['status'] = value

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
    def signature(self):
        data = {'seller': self.seller, 'creditor': self.creditor}
        data.update(**self.payload)
        value = generate_signature(data)
        return value

    @signature.setter
    def signature(self, _):
        raise NotImplementedError

    @signature.deleter
    def signature(self):
        raise NotImplementedError

    @property
    def data(self):
        value = {**{
            'id': self.id, 'ttl': self.ttl
        }, **self.__data}
        return value

    @data.setter
    def data(self, _):
        raise NotImplementedError

    @data.deleter
    def data(self):
        raise NotImplementedError

    def exist(self):
        keys = self.__db.keys(self.__name)
        count = len(keys)
        return count == 1

    def save(self, expire=None):
        if not self.exist():
            self.__data['status'] = Transaction.STATUS.awaiting
        value = json.dumps(self.__data)
        ex = self.ttl if self.exist() else expire or 60
        self.__db.set(self.__name, value, ex=ex)

    def delete(self):
        self.__db.delete(*[self.__name])
        self.__data = self.__DEFAULT_DATA % Transaction.STATUS.no_exist

    def __str__(self):
        return self.__name

    def __repr__(self):
        value = json.dumps(self.data)
        return value
