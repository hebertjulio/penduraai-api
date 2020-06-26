import json

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from model_utils.models import TimeStampedModel
from model_utils import Choices


class Transaction(TimeStampedModel):

    STATUS = Choices(
        ('not_used', _('not used')),
        ('used', _('used')),
        ('discarded', _('discarded')),
    )

    id = models.BigAutoField(primary_key=True, editable=False)
    scope = models.CharField(_('scope'), max_length=30)
    data = models.TextField(('data'), blank=True)
    expire_at = models.DateTimeField(_('expire at'))

    user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='usertransactions',
    )

    profile = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE,
        related_name='profiletransactions',
    )

    status = models.CharField(
        _('status'), max_length=30, db_index=True,
        choices=STATUS, default=STATUS.not_used
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

    def is_expired(self):
        return bool(self.ttl < 1)

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    def __str__(self):
        return 'ID. %s' % self.id

    def __repr__(self):
        return 'ID. %s' % self.id

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')
