from json import loads, dumps
from datetime import timedelta
from uuid import uuid4

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from redis import from_url

from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST

from .services import get_signature, token_encode


class Ticket:

    db = from_url(
        settings.BRIDGES_REDIS_URL, db=None, **{
            'decode_responses': True})

    def __init__(self, id_=None):
        self.id = id_ or str(uuid4())

    @property
    def name(self):
        name = 'ticket:' + self.id
        return name

    @name.setter
    def name(self, value):  # skipcq
        raise NotImplementedError

    @property
    def scope(self):
        dataset = self.db.hgetall(self.name) or {}
        value = dataset.get('scope', '')
        return value

    @scope.setter
    def scope(self, value):
        if not isinstance(value, str):
            raise ValueError
        dataset = self.db.hgetall(self.name) or {}
        dataset.update({'scope': value})
        self.db.hmset(self.name, dataset)

    @property
    def data(self):
        dataset = self.db.hgetall(self.name) or {}
        value = dataset.get('data', {})
        return loads(value)

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError
        dataset = self.db.hgetall(self.name) or {}
        dataset.update({'data': dumps(value)})
        self.db.hmset(self.name, dataset)

    @property
    def usage(self):
        dataset = self.db.hgetall(self.name) or {}
        value = dataset.get('usage', -2)
        return int(value)

    @usage.setter
    def usage(self, value):
        if not isinstance(value, int):
            raise ValueError
        dataset = self.db.hgetall(self.name) or {}
        dataset.update({'usage': value})
        self.db.hmset(self.name, dataset)

    @property
    def signature(self):
        signature = get_signature(self.data, self.scope)
        return signature

    @signature.setter
    def signature(self, value):  # skipcq
        raise NotImplementedError

    @property
    def token(self):
        expire = timezone.now() + timedelta(seconds=self.expire)
        data = {'id': self.id}
        token = token_encode(data, expire)
        return token

    @token.setter
    def token(self, value):  # skipcq
        raise NotImplementedError

    @property
    def expire(self):
        expire = self.db.ttl(self.name)
        return expire

    @expire.setter
    def expire(self, value):
        if not isinstance(value, int):
            raise ValueError
        self.db.expire(self.name, value)

    def exist(self, raise_exception=False):
        keys = self.db.keys(*[self.name])
        exist = len(keys) > 0
        if raise_exception and not exist:
            raise self.DoesNotExist
        return exist

    class DoesNotExist(APIException):

        status_code = HTTP_400_BAD_REQUEST
        default_code = 'invalid'
        default_detail = _('Ticket does not exist.')
