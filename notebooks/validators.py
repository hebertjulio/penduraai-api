from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .services import generate_signature
from .dictdb import Transaction


class IsCustomerRecordOwnerValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        if value.debtor.id != user.id:
            message = _('You aren\'t owner of this customer record.')
            raise serializers.ValidationError(message)


class CustomerFromYourselfValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        if value['creditor'].id == user.id:
            message = _('You can\'t customer from yourself.')
            raise serializers.ValidationError(message)


class AlreadyACustomerValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        qs = user.as_debtor.filter(creditor=value['creditor'])
        if qs.exists():
            message = _('You are already a customer.')
            raise serializers.ValidationError(message)


class SellerAccountableValidator:

    def __call__(self, value):
        customer_record = value['customer_record']
        qs = customer_record.creditor.accountable.filter(
            id=value['seller'].id
        )
        if not qs.exists():
            message = _('Accountable for seller is invalid.')
            raise serializers.ValidationError(message)


class BuyerAccountableValidator:

    def __call__(self, value):
        customer_record = value['customer_record']
        qs = customer_record.debtor.accountable.filter(
            id=value['buyer'].id
        )
        if not qs.exists():
            message = _('Accountable for buyer is invalid.')
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
        parent = serializer_field.parent
        data = {
            k: v for k, v in parent.initial_data.items()
            if k in tran.payload.keys()
        }
        signature = generate_signature(tran.creditor, data)
        if tran.signature != signature:
            message = _('Invalid transaction signature.')
            raise serializers.ValidationError(message)


class TransactionStatusValidator:

    def __call__(self, value):
        tran = Transaction(str(value))
        if tran.status != Transaction.STATUS.awaiting:
            message = _('Transaction status is %s.' % tran.status)
            raise serializers.ValidationError(message)
