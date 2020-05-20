from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel
from model_utils import Choices


class Transaction(TimeStampedModel):

    STATUS = Choices(
        ('done', _('done')),
        ('fail', _('fail')),
    )

    TYPE = Choices(
        ('credit', _('credit')),
        ('debit', _('debit')),
    )

    uuid = models.UUIDField(unique=True, editable=False)
    description = models.TextField(('description'))
    value = models.DecimalField(_('value'), max_digits=10,  decimal_places=2)

    type = models.CharField(
        _('type'), max_length=30, db_index=True, choices=TYPE
    )

    creditor = models.ForeignKey(
        'accounts.User', related_name='creditor', on_delete=models.CASCADE
    )

    debtor = models.ForeignKey(
        'accounts.User', related_name='debtor', on_delete=models.CASCADE
    )

    requester = models.ForeignKey(
        'accounts.Profile', related_name='requester', on_delete=models.CASCADE
    )

    signature = models.ForeignKey(
        'accounts.Profile', related_name='signature', on_delete=models.CASCADE
    )

    status = models.CharField(
        _('status'), max_length=30, db_index=True, choices=STATUS
    )

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')
