import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from model_utils.models import TimeStampedModel
from model_utils import Choices


class Record(TimeStampedModel):

    TYPE = Choices(
        ('payment', _('payment')),
        ('sale', _('sale')),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    description = models.CharField(('description'), max_length=255)

    value = models.DecimalField(
        _('value'), max_digits=10, decimal_places=2,
        validators=[
            MinValueValidator(0.01)
        ]
    )

    type = models.CharField(
        _('type'), max_length=30, db_index=True,
        choices=TYPE
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


class Whitelist(TimeStampedModel):

    STATUS = Choices(
        ('authorized', _('authorized')),
        ('unauthorized', _('unauthorized')),
    )

    creditor = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='whitelists_creditor',
    )

    debtor = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='whitelists_debtor',
    )

    status = models.CharField(
        _('status'), max_length=30, db_index=True,
        choices=STATUS
    )

    def __str__(self):
        return self.creditor.name

    def __repr__(self):
        return self.creditor.name

    class Meta:
        verbose_name = _('whitelist')
        verbose_name_plural = _('whitelists')
        unique_together = [
            ['creditor', 'debtor']
        ]
