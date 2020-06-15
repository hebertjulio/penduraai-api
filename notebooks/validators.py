from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .services import generate_signature
from .dictdb import Transaction


class IsStoreCustomerValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        qs = request.user.customer.filter(
            store=value, is_authorized=True
        )
        if not qs.exists():
            message = _('You aren\'t customer of this store.')
            raise serializers.ValidationError(message)


class CustomerOfYourStoreValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        if value.id == user.id:
            message = _('You can\'t customer of your store.')
            raise serializers.ValidationError(message)


class AlreadyStoreCustomerValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        qs = user.customer.filter(store=value)
        if qs.exists():
            message = _('You are already a customer of this store.')
            raise serializers.ValidationError(message)


class IsStoreAttendantValidator:

    def __call__(self, value):
        qs = value['store'].profiles.filter(
            id=value['attendant'].id, is_active=True
        )
        if not qs.exists():
            message = _('Attendant isn\'t store profile.')
            raise serializers.ValidationError(message)


class TransactionExistValidator:

    def __call__(self, value):
        tran = Transaction(str(value))
        if not tran.exist():
            message = _('Transaction non-existent.')
            raise serializers.ValidationError(message)


class TransactionSignatureValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        tran = Transaction(str(value))
        if not tran.exist():
            return None
        parent = serializer_field.parent
        data = {
            k: v for k, v in parent.initial_data.items()
            if k != 'transaction'
        }
        signature = generate_signature(data)
        if tran.signature != signature:
            message = _('Invalid transaction signature.')
            raise serializers.ValidationError(message)


class TransactionStatusValidator:

    def __call__(self, value):
        tran = Transaction(str(value))
        if not tran.exist():
            return None
        if tran.status != Transaction.STATUS.awaiting:
            message = _('Transaction status is %s.' % tran.status)
            raise serializers.ValidationError(message)
