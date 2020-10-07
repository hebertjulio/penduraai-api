from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel
from model_utils import Choices


class Transaction(TimeStampedModel):

    SCOPE = Choices(
        ('profile', _('profile')),
        ('sheet', _('sheet')),
        ('record', _('record')),
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    scope = models.CharField(
        _('scope'), choices=SCOPE, max_length=50, db_index=True)
    data = models.TextField(_('data'), default='{}', blank=True)
    expire_in = models.DateTimeField(_('expire in'), db_index=True)
    max_usage = models.SmallIntegerField(_('max usage'), default=1)
    usage = models.SmallIntegerField(_('usage'), default=0)

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')
