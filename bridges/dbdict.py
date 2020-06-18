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
        'awaiting', 'accepted', 'rejected',
    ]

    PREFIX = 'transaction'

    DEFAULT = """
        {"scope": null, "data": {}, "status": "awaiting"}
    """

    client = redis.from_url(settings.TRANSACTION_REDIS_URL)

    def __init__(self, token=None):
        if token is None:
            token = urlsafe_base64_encode(
                force_bytes(str(uuid.uuid4())))
        self.token = token
        self.load()
        if not self.exist():
            self.save()

    @property
    def name(self):
        name = ':'.join([self.PREFIX, self.token])
        return name

    @property
    def scope(self):
        if 'scope' in self.dataset.keys():
            value = self.dataset['scope']
            return value
        return None

    @scope.setter
    def scope(self, value):
        if value not in self.SCOPES:
            raise ValueError
        self.dataset.update({'scope': value})

    @property
    def data(self):
        if 'data' in self.dataset.keys():
            value = self.dataset['data']
            return value
        return {}

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError
        self.dataset.update({'data': value})

    @property
    def status(self):
        if 'status' in self.dataset.keys():
            value = self.dataset['status']
            return value
        return None

    @status.setter
    def status(self, value):
        if value not in self.STATUS:
            raise ValueError
        self.dataset.update({'status': value})

    @property
    def ttl(self):
        value = self.client.ttl(self.name)
        return value

    @ttl.setter
    def ttl(self, expire):
        self.client.expire(self.name, expire)

    def exist(self):
        keys = self.client.keys(self.name)
        count = len(keys)
        return count == 1

    def load(self):
        value = self.client.get(self.name)
        value = value or self.DEFAULT
        self.dataset = json.loads(value)

    def save(self):
        value = json.dumps(self.dataset, cls=DecimalEncoder)
        ex = self.ttl if self.exist() else 60
        self.client.set(self.name, value, ex=ex)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __iter__(self):
        dataset = {**self.dataset, **{'token': self.token}}
        for key, value in dataset.items():
            yield key, value
