import json

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from model_utils.models import TimeStampedModel
from model_utils import Choices


class Transaction(TimeStampedModel):

    SCOPE = Choices(
        ('record', _('record')),
        ('sheet', _('sheet')),
        ('profile', _('profile')),
    )

    id = models.BigAutoField(primary_key=True, editable=False)
    data = models.TextField(('data'), blank=True)
    expire_at = models.DateTimeField(_('expire at'))
    discarded = models.BooleanField(_('discarded'), default=False)

    user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='usertransactions',
    )

    profile = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE,
        related_name='profiletransactions',
    )

    scope = models.CharField(
        _('scope'), max_length=30, db_index=True,
        choices=SCOPE
    )

    @property
    def ttl(self):
        diff = self.expire_at - timezone.now()
        ttl = round(diff.total_seconds())
        return ttl

    def get_data(self):
        if self.data.strip():
            return json.loads(self.data)
        return {}

    @property
    def expired(self):
        return bool(self.ttl < 1)

    @property
    def used(self):
        related_name = 'transaction' + self.scope
        return hasattr(self, related_name)

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
