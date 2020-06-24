import json

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from model_utils.models import TimeStampedModel
from model_utils import Choices


class Transaction(TimeStampedModel):

    STATUS = Choices(
        ('awaiting', _('awaiting')),
        ('accepted', _('accepted')),
        ('rejected', _('rejected')),
    )

    id = models.BigAutoField(primary_key=True, editable=False)
    scope = models.CharField(_('scope'), max_length=30)
    data = models.TextField(('data'), blank=True)
    expire_at = models.DateTimeField(_('expire at'))

    status = models.CharField(
        _('status'), max_length=30, db_index=True,
        choices=STATUS, default=STATUS.awaiting
    )

    @property
    def datajson(self):
        if self.data.strip():
            return json.loads(self.data)
        return {}

    @property
    def ttl(self):
        diff = self.expire_at - timezone.now()
        ttl = round(diff.total_seconds())
        return ttl

    def is_expired(self):
        return self.ttl < 1

    def __repr__(self):
        return 'Transaction %s' % self.id

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')
