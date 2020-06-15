from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from model_utils.models import TimeStampedModel
from model_utils import Choices

from .querysets import SheetQuerySet


class Record(TimeStampedModel):

    OPERATION = Choices(
        ('credit', _('credit')),
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

    sheet = models.ForeignKey(
        'Sheet', on_delete=models.CASCADE,
        related_name='records',
    )

    attendant = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE,
        related_name='attendant',
    )

    subscriber = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE,
        related_name='subscriber',
    )

    is_deleted = models.BooleanField(
        _('deleted status'),
        default=False,
        help_text=_(
            'Designates whether this record should be treated as deleted. '
            'Select this instead of deleting record.'
        ),
    )

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    class Meta:
        verbose_name = _('record')
        verbose_name_plural = _('records')


class Sheet(TimeStampedModel):

    id = models.BigAutoField(primary_key=True, editable=False)

    store = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='store',
    )

    customer = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='customer',
    )

    is_authorized = models.BooleanField(
        _('authorized status'), default=True
    )

    def __str__(self):
        return 'No. %s' % self.id

    def __repr__(self):
        return 'No. %s' % self.id

    objects = SheetQuerySet.as_manager()

    class Meta:
        verbose_name = _('sheet')
        verbose_name_plural = _('sheets')
        unique_together = [
            ['store', 'customer']
        ]
