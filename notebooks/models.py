from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from model_utils.models import TimeStampedModel
from model_utils import Choices

from .querysets import CustomerQuerySet


class Record(TimeStampedModel):

    OPERATION = Choices(
        ('payment', _('payment')),
        ('debt', _('debt')),
    )

    id = models.BigAutoField(primary_key=True, editable=False)
    note = models.CharField(('note'), max_length=255, blank=True)

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
        related_name='records_creditor',
    )

    debtor = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='records_debtor',
    )

    seller = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE,
        related_name='records_seller',
    )

    buyer = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE,
        related_name='records_buyer',
    )

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    class Meta:
        verbose_name = _('record')
        verbose_name_plural = _('records')


class Customer(TimeStampedModel):

    id = models.BigAutoField(primary_key=True, editable=False)

    creditor = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='customers_creditor',
    )

    debtor = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='customers_debtor',
    )

    authorized = models.BooleanField(_('authorized'), default=True)

    def __str__(self):
        return self.creditor.name

    def __repr__(self):
        return self.creditor.name

    objects = CustomerQuerySet.as_manager()

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')
        unique_together = [
            ['creditor', 'debtor']
        ]
