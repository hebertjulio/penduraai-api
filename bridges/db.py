from json import loads, dumps

from django.conf import settings

from jwt import encode as jwt_encode

from redis import from_url

from .services import generate_signature


class Ticket:

    prefix = 'ticket'
    db = from_url(settings.BRIDGES_REDIS_URL)

    def __init__(self, key, scope, expire=30):
        self.scope = scope
        self.key = key
        self.expire = expire

    @property
    def name(self):
        name = 'ticket:%s:%s' % (self.scope, self.key)
        return name

    @name.setter
    def name(self, value):  # skipcq
        raise NotImplementedError

    @property
    def signature(self):
        values = self.data.values()
        signature = generate_signature(values)
        return signature

    @property
    def data(self):
        value = self.db.get(self.name) or '{}'
        value = loads(value)
        return value

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError
        value = dumps(value)
        ttl = self.db.ttl(self.name)
        expire = ttl if ttl > 0 else self.expire
        self.db.set(self.name, value, ex=expire)

    @property
    def token(self):
        data = {'key': self.key, 'scope': self.scope, 'aud': 'ticket'}
        value = jwt_encode(data, settings.SECRET_KEY, algorithm='HS256')
        value = value.decode('utf-8')
        return value

    @property
    def ttl(self):
        value = self.db.ttl(self.name)
        return value

    def exist(self):
        ttl = self.db.ttl(self.name)
        return ttl > 0

    def discard(self):
        self.db.delete(*[self.name])
