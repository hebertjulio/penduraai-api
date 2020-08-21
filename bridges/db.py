from json import loads, dumps
from uuid import uuid4

from django.conf import settings

from jwt import encode as jwt_encode
from redis import from_url

from .services import get_signature


class Ticket:

    __db = from_url(settings.BRIDGES_REDIS_URL)
    __data = {}

    def __init__(self, scope, key=None):
        self.scope = scope
        self.key = key or str(uuid4())

    @property
    def name(self):
        name = 'ticket:%s:%s' % (self.scope, self.key)
        return name

    @name.setter
    def name(self, value):  # skipcq
        raise NotImplementedError

    @property
    def signature(self):
        signature = get_signature(self.data, self.scope)
        return signature

    @property
    def data(self):
        data = self.__db.get(self.name)
        data = loads(data) if data else self.__data
        return data

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError
        self.__data = value

    @property
    def token(self):
        data = {'key': self.key, 'scope': self.scope, 'aud': 'ticket'}
        token = jwt_encode(data, settings.SECRET_KEY, algorithm='HS256')
        token = token.decode('utf-8')
        return token

    def exist(self, raise_exception=False):
        keys = self.__db.keys(*[self.name])
        exist = len(keys) > 0
        if raise_exception and not exist:
            raise self.DoesNotExist
        return exist

    def persist(self, expire=None):
        if expire is None and self.exist():
            expire = self.__db.ttl(self.name)
        data = dumps(self.data)
        self.__db.set(self.name, data, ex=expire)

    def discard(self):
        self.__db.delete(*[self.name])

    class DoesNotExist(Exception):

        def __init__(self):
            super().__init__('Ticket does not exist.')
