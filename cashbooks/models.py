from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from model_utils.models import TimeStampedModel
from model_utils import Choices


class Transaction(TimeStampedModel):

    OPERATION = Choices(
        ('credit', _('credit')),
        ('debit', _('debit')),
    )

    description = models.TextField(('description'))

    value = models.DecimalField(
        _('value'), max_digits=10, decimal_places=2,
        validators=[
            MinValueValidator(0.01)
        ]
    )

    operation = models.CharField(
        _('operation'), max_length=30, db_index=True,
        choices=OPERATION
    )

    creditor = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='transactions_creditor',
    )

    debtor = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='transactions_debtor',
    )

    requester = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE,
        related_name='transactions_requester',
    )

    signatory = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE,
        related_name='transactions_signatory',
    )

    def __str__(self):
        return '%s %s %s' % (
            self.creditor, self.value, self.operation.upper(),)

    def __repr__(self):
        return '%s %s %s' % (
            self.creditor, self.value, self.operation.upper(),)

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')


class Whitelist(TimeStampedModel):

    STATUS = Choices(
        ('authorized', _('authorized')),
        ('unauthorized', _('unauthorized')),
    )

    owner = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='whitelists_owner',
    )

    customer = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='whitelists_customer',
    )

    status = models.CharField(
        _('status'), max_length=30, db_index=True,
        choices=STATUS
    )

    def __str__(self):
        return self.guest.name

    def __repr__(self):
        return self.guest.name

    class Meta:
        verbose_name = _('whitelist')
        verbose_name_plural = _('whitelists')
        unique_together = [
            ['owner', 'customer']
        ]
