from rest_framework import serializers

from .models import Transaction

from .validators import (
    TrasactionStatusValidator, TransactionExpiredValidator,
    TransactionIntegrityValidator, TrasactionScopeValidator)


class TransactionRelatedField(serializers.PrimaryKeyRelatedField):

    queryset = Transaction.objects.all()
    write_only = True

    def __init__(self, *args, **kwargs):
        self.scope = kwargs.pop('scope')
        if self.scope is None:
            raise ValueError
        super().__init__(*args, **kwargs)

    def get_validators(self):
        validators = [
            TransactionIntegrityValidator(),
            TrasactionStatusValidator(),
            TransactionExpiredValidator(),
            TrasactionScopeValidator(self.scope)
        ]
        return validators
