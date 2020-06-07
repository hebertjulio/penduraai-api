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

    customer_record = models.ForeignKey(
        'CustomerRecord', on_delete=models.CASCADE,
        related_name='customer_record',
    )

    seller = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE,
        related_name='as_seller',
    )

    buyer = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE,
        related_name='as_buyer',
    )

    strikethrough = models.BooleanField(_('strikethrough'), default=False)

    @property
    def creditor(self):
        return self.customer_record.creditor.name

    @creditor.setter
    def creditor(self, _):
        raise NotImplementedError

    @creditor.deleter
    def creditor(self):
        raise NotImplementedError

    @property
    def debtor(self):
        return self.customer_record.debtor.name

    @debtor.setter
    def debtor(self, _):
        raise NotImplementedError

    @debtor.deleter
    def debtor(self):
        raise NotImplementedError

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    class Meta:
        verbose_name = _('record')
        verbose_name_plural = _('records')


class CustomerRecord(TimeStampedModel):

    id = models.BigAutoField(primary_key=True, editable=False)

    creditor = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='as_creditor',
    )

    debtor = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='as_debtor',
    )

    authorized = models.BooleanField(_('authorized'), default=True)

    def __str__(self):
        return self.debtor.name

    def __repr__(self):
        return self.debtor.name

    objects = CustomerQuerySet.as_manager()

    class Meta:
        verbose_name = _('customer record')
        verbose_name_plural = _('customer records')
        unique_together = [
            ['creditor', 'debtor']
        ]
