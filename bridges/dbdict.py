import redis
import json
import uuid

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.conf import settings

from .encoders import DecimalEncoder


class Transaction:

    SCOPES = [
        'profile', 'sheet', 'record',
    ]

    STATUS = [
        'no_exist', 'awaiting', 'accepted', 'rejected',
    ]

    PREFIX = 'transaction'

    def __init__(self, token=None):
        if token is None:
            token = urlsafe_base64_encode(force_bytes(str(uuid.uuid4())))
        self.__client = redis.from_url(settings.TRANSACTION_REDIS_URL)
        self.__name = ':'.join([self.PREFIX, token])
        data = self.__client.get(self.__name)
        self.__data = json.loads(data or '{}')

    @property
    def token(self):
        value = self.__name.split(':')[1]
        return value

    @property
    def scope(self):
        if 'scope' in self.__data.keys():
            value = self.__data['scope']
            return value
        return None

    @scope.setter
    def scope(self, value):
        if value not in self.SCOPES:
            raise ValueError
        self.__data.update({'scope': value})

    @property
    def payload(self):
        if 'payload' in self.__data.keys():
            value = self.__data['payload']
            return value
        return {}

    @payload.setter
    def payload(self, value):
        if not isinstance(value, dict):
            raise ValueError
        self.__data.update({'payload': value})

    @property
    def status(self):
        if 'status' in self.__data.keys():
            value = self.__data['status']
            return value
        return None

    @status.setter
    def status(self, value):
        if value not in self.STATUS:
            raise ValueError
        self.__data.update({'status': value})

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
            self.__data['status'] = 'awaiting'
        value = json.dumps(self.__data, cls=DecimalEncoder)
        ex = self.ttl if self.exist() else expire or 60
        self.__client.set(self.__name, value, ex=ex)

    def delete(self):
        self.__client.delete(*[self.__name])
        self.__data = {}

    def __str__(self):
        return self.__name

    def __repr__(self):
        value = json.dumps(self.data)
        return value
