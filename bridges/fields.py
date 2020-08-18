from django.utils.translation import gettext_lazy as _

from rest_framework.validators import ValidationError
from rest_framework.fields import Field

from .services import decode_token
from .models import Transaction

from .validators import (
    TransactionExpiredValidator, TransactionSignatureValidator,
    TransactionTicketsValidator)


class TransactionTokenField(Field):

    validators = [
        TransactionExpiredValidator(),
        TransactionSignatureValidator(),
        TransactionTicketsValidator()
    ]

    def to_representation(self, instance):
        print(instance)
        return instance

    def to_internal_value(self, data):
        try:
            payload = decode_token(data)
            obj = Transaction.objects.get(pk=payload['id'])
            return obj
        except (
                TypeError,
                Transaction.DoesNotExist):
            raise ValidationError(_('Transaction does not exist.'))
