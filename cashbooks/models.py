from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel
from model_utils import Choices


class Transaction(TimeStampedModel):

    OPERATION = Choices(
        ('credit', _('credit')),
        ('debit', _('debit')),
    )

    description = models.TextField(('description'))
    value = models.DecimalField(_('value'), max_digits=10,  decimal_places=2)

    operation = models.CharField(
        _('operation'), max_length=30, db_index=True, choices=OPERATION)
    creditor = models.ForeignKey(
        'accounts.User', related_name='creditor', on_delete=models.CASCADE)
    debtor = models.ForeignKey(
        'accounts.User', related_name='debtor', on_delete=models.CASCADE)
    requester = models.ForeignKey(
        'accounts.Profile', related_name='requester', on_delete=models.CASCADE)
    signature = models.ForeignKey(
        'accounts.Profile', related_name='signature', on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')
