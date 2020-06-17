import redis
import json

from django.utils.translation import gettext_lazy as _
from django.conf import settings

from model_utils import Choices

from .encoders import DecimalEncoder


class Transaction:

    SCOPE = Choices(
        ('profile', _('profile')),
        ('sheet', _('sheet')),
        ('record', _('record')),
    )

    STATUS = Choices(
        ('no_exist', _('no exist')),
        ('awaiting', _('awaiting')),
        ('accepted', _('accepted')),
        ('rejected', _('rejected')),
    )

    PREFIX = 'transaction'

    __DEFAULT_DATA = '''{
        "payload": {}, "scope": "", "status": "%s"
    }'''

    def __init__(self, token):
        self.__client = redis.from_url(settings.TRANSACTION_REDIS_URL)
        self.__name = ':'.join([self.PREFIX, token])
        data = self.__client.get(self.__name)
        data = data or self.__DEFAULT_DATA % Transaction.STATUS.no_exist
        self.__data = json.loads(data)

    @property
    def token(self):
        value = self.__name.split(':')[1]
        return value

    @property
    def scope(self):
        value = self.__data['scope']
        return value

    @scope.setter
    def scope(self, value):
        if value not in self.SCOPE:
            raise ValueError
        self.__data['scope'] = value

    @property
    def payload(self):
        value = self.__data['payload']
        return value

    @payload.setter
    def payload(self, value):
        if not isinstance(value, dict):
            raise ValueError
        self.__data['payload'] = value

    @property
    def status(self):
        value = self.__data['status']
        return value

    @status.setter
    def status(self, value):
        if value not in self.STATUS:
            raise ValueError
        self.__data['status'] = value

    @property
    def ttl(self):
        value = self.__client.ttl(self.__name)
        return value

    @property
    def data(self):
        value = {**{
            'token': self.token, 'ttl': self.ttl
        }, **self.__data}
        return value

    def exist(self):
        keys = self.__client.keys(self.__name)
        count = len(keys)
        return count == 1

    def save(self, expire=None):
        if not self.exist():
            self.__data['status'] = Transaction.STATUS.awaiting
        value = json.dumps(self.__data, cls=DecimalEncoder)
        ex = self.ttl if self.exist() else expire or 60
        self.__client.set(self.__name, value, ex=ex)

    def delete(self):
        self.__client.delete(*[self.__name])
        self.__data = self.__DEFAULT_DATA % Transaction.STATUS.no_exist

    def __str__(self):
        return self.__name

    def __repr__(self):
        value = json.dumps(self.data)
        return value
