from json import loads

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

from jwt import encode as jwt_encode

from model_utils.models import TimeStampedModel
from model_utils import Choices


class Transaction(TimeStampedModel):

    STATUS = Choices(
        ('unused', _('unused')),
        ('used', _('used')),
        ('discarded', _('discarded')),
    )

    AUDIENCE = 'v1'

    id = models.BigAutoField(primary_key=True, editable=False)
    data = models.TextField(('data'), blank=True)
    expire_at = models.DateTimeField(_('expire at'))

    status = models.CharField(
        _('status'), max_length=30, db_index=True,
        choices=STATUS, default=STATUS.unused
    )

    @property
    def data_as_dict(self):
        value = loads(self.data)
        return value

    @property
    def token(self):
        payload = {'id': self.id, 'aud': self.AUDIENCE, 'exp': self.expire_at}
        token = jwt_encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

    @property
    def expired(self):
        delta = self.expire_at - timezone.now()
        return bool(delta.total_seconds() < 1)

    @property
    def signature(self):
        data = loads(self.data)
        items = sorted(data.items())
        value = ''.join([key + str(value) for key, value in items])
        return value

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
