import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from model_utils.models import TimeStampedModel
from model_utils import Choices


class Record(TimeStampedModel):

    OPERATION = Choices(
        ('payment', _('payment')),
        ('debt', _('debt')),
    )

    STATUS = Choices(
        ('accepted', _('accepted')),
        ('rejected', _('rejected')),
    )

    MIN_VALUE = 0.01

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(('description'), max_length=255)

    value = models.DecimalField(
        _('value'), max_digits=10, decimal_places=2,
        validators=[
            MinValueValidator(MIN_VALUE)
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

    status = models.CharField(
        _('status'), max_length=30, db_index=True,
        choices=STATUS
    )

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    class Meta:
        verbose_name = _('record')
        verbose_name_plural = _('records')


class Customer(TimeStampedModel):

    creditor = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='customers_creditor',
    )

    debtor = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='customers_debtor',
    )

    authorized = models.BooleanField(_('authorized'))

    def __str__(self):
        return self.creditor.name

    def __repr__(self):
        return self.creditor.name

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')
        unique_together = [
            ['creditor', 'debtor']
        ]
