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
        related_name='sheetrecords',
    )

    attendant = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE,
        related_name='attendantrecords',
    )

    signature = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE,
        related_name='signaturerecords',
    )

    is_active = models.BooleanField(
        _('active status'),
        default=True,
        help_text=_(
            'Designates whether this record should be treated as active. '
            'Unselect this instead of deleting record.'
        ),
    )

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    def __repr__(self):
        return 'Record %s' % self.id

    class Meta:
        verbose_name = _('record')
        verbose_name_plural = _('records')


class Sheet(TimeStampedModel):

    id = models.BigAutoField(primary_key=True, editable=False)

    store = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='storesheets',
    )

    customer = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='customersheets',
    )

    buyers = models.ManyToManyField(
        'accounts.Profile', through='Buyer', related_name='buyersheets'
    )

    is_active = models.BooleanField(
        _('active status'),
        default=True,
        help_text=_(
            'Designates whether this sheet should be treated as active. '
            'Unselect this instead of deleting sheet.'
        ),
    )

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    def __repr__(self):
        return 'Sheet %s' % self.id

    objects = SheetQuerySet.as_manager()

    class Meta:
        verbose_name = _('sheet')
        verbose_name_plural = _('sheets')
        unique_together = [
            ['store', 'customer']
        ]


class Buyer(TimeStampedModel):

    id = models.BigAutoField(primary_key=True, editable=False)

    sheet = models.ForeignKey(
        'Sheet', on_delete=models.CASCADE,
        related_name='sheetbuyers',
    )

    profile = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE,
        related_name='profilebuyers',
    )

    def __repr__(self):
        return 'Buyer %s' % self.id

    class Meta:
        verbose_name = _('buyer')
        verbose_name_plural = _('buyers')
        unique_together = [
            ['sheet', 'profile']
        ]
