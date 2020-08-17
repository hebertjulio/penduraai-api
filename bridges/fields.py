from django.utils.translation import gettext_lazy as _

from rest_framework.validators import ValidationError
from rest_framework.fields import Field

from .services import get_payload
from .models import Transaction

from .validators import (
    TransactionExpiredValidator, TransactionSignatureValidator,
    TransactionUsageValidator)


class TransactionField(Field):

    validators = [
        TransactionExpiredValidator(),
        TransactionSignatureValidator(),
        TransactionUsageValidator()
    ]

    def to_representation(self, instance):
        print(instance)
        return instance

    def to_internal_value(self, data):
        try:
            payload = get_payload(data)
            obj = Transaction.objects.get(pk=payload['id'])
            return obj
        except (
                TypeError,
                Transaction.DoesNotExist):
            raise ValidationError(_('Transaction does not exist.'))
