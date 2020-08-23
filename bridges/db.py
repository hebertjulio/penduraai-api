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
        return self.get_hm('scope')

    @scope.setter
    def scope(self, value):
        if not isinstance(value, str):
            raise ValueError
        self.set_hm('scope', value)

    @property
    def data(self):
        return loads(self.get_hm('data'))

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError
        self.set_hm('data', dumps(value))

    @property
    def status(self):
        return self.get_hm('status')

    @status.setter
    def status(self, value):
        if not isinstance(value, str):
            raise ValueError
        self.set_hm('status', value)

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
        return self.db.ttl(self.name)

    @expire.setter
    def expire(self, value):
        if not isinstance(value, int):
            raise ValueError
        self.db.expire(self.name, value)

    def set_hm(self, attr, value):
        if not isinstance(value, str):
            raise ValueError
        hm = self.db.hgetall(self.name) or {}
        hm.update({attr: value})
        self.db.hmset(self.name, hm)

    def get_hm(self, attr):
        hm = self.db.hgetall(self.name) or {}
        return hm.get(attr, None)

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
