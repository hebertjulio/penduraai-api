from json import loads

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from model_utils.models import TimeStampedModel
from model_utils.choices import Choices

from .services import generate_signature, token_encode


class Ticket(TimeStampedModel):

    SCOPE = Choices(
        ('profile', _('profile')),
        ('sheet', _('sheet')),
        ('record', _('record')),
    )

    id = models.BigAutoField(primary_key=True, editable=False)
    payload = models.TextField(('payload'), default='{}')
    scope = models.CharField(('scope'), choices=SCOPE, max_length=30)
    expire_at = models.DateTimeField(_('expire at'))
    usage = models.SmallIntegerField(_('usage'), default=0)

    @property
    def payload_as_dict(self):
        value = loads(self.payload)
        return value

    @property
    def token(self):
        payload = {'id': self.id, 'exp': self.expire_at}
        token = token_encode(payload)
        return token

    @property
    def signature(self):
        values = self.payload_as_dict.values()
        value = generate_signature(values)
        return value

    @property
    def expired(self):
        delta = self.expire_at - timezone.now()
        return bool(delta.total_seconds() < 1)

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    def __str__(self):
        return 'Ticket %s' % self.id

    def __repr__(self):
        return 'Ticket %s' % self.id

    class Meta:
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')
