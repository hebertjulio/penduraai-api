from redis import Redis

from django.conf import settings


class Storage:

    class Item:

        def __init__(self, value, expire=60):
            self.value = value
            self.expire = expire

        def __getattr__(self, instance):
            return self.value

        def __str__(self):
            return self.value

        def __repr__(self):
            return self.value

    PREFIX = 'storage'

    def __init__(self, uuid):
        host = settings.DICTDB_REDIS_HOST
        port = settings.DICTDB_REDIS_PORT
        db = settings.DICTDB_REDIS_DB
        self.db = Redis(host=host, port=port, db=db)
        self.uuid = uuid

    def __setitem__(self, key, value):
        if not isinstance(value, Storage.Item):
            raise TypeError('value must be Storage.Item')
        name = ':'.join([self.PREFIX, self.uuid, key])
        self.db.set(name, str(value), ex=value.expire)

    def __getitem__(self, key):
        name = ':'.join([self.PREFIX, self.uuid, key])
        value = self.db.get(name)
        return value

    def __delitem__(self, key):
        name = ':'.join([self.PREFIX, self.uuid, key])
        self.db.delete(name)

    def __len__(self):
        name = ':'.join([self.PREFIX, self.uuid, '*'])
        names = self.db.keys(name)
        count = len(names)
        return count

    def __contains__(self, key):
        names = ':'.join([self.PREFIX, self.uuid, key])
        count = self.db.exists(*names)
        return count == 1

    def __delattr__(self, instance):
        patterns = ':'.join([self.PREFIX, self.uuid, '*'])
        names = self.db.keys(patterns)
        self.db.delete(*names)
