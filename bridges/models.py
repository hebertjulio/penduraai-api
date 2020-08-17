from json import loads

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

from jwt import encode as jwt_encode

from model_utils.models import TimeStampedModel

from .services import get_signature


class Transaction(TimeStampedModel):

    id = models.BigAutoField(primary_key=True, editable=False)
    data = models.TextField(('data'), blank=True)
    expire_at = models.DateTimeField(_('expire at'))
    max_usage = models.SmallIntegerField(_('max usage'), default=1)
    usage = models.SmallIntegerField(_('usage'), default=1)

    @property
    def data_as_dict(self):
        value = loads(self.data)
        return value

    @property
    def token(self):
        payload = {'id': self.id, 'aud': 'v1', 'exp': self.expire_at}
        token = jwt_encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

    @property
    def signature(self):
        fields = [field for field in self.data_as_dict.keys()]
        value = get_signature(fields, self.data_as_dict)
        return value

    @property
    def expired(self):
        delta = self.expire_at - timezone.now()
        return bool(delta.total_seconds() < 1)

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    def __str__(self):
        return 'Transaction %s' % self.id

    def __repr__(self):
        return 'Transaction %s' % self.id

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')
