from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .services import generate_signature
from .dictdb import Transaction


class IsSheetOwnerValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        if value.customer.id != user.id:
            message = _('You aren\'t owner of this sheet.')
            raise serializers.ValidationError(message)


class CustomerFromYourselfValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        if value['store'].id == user.id:
            message = _('You can\'t customer from yourself.')
            raise serializers.ValidationError(message)


class AlreadyACustomerValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        qs = user.customer.filter(store=value['store'])
        if qs.exists():
            message = _('You are already a customer.')
            raise serializers.ValidationError(message)


class AttendantAccountableValidator:

    def __call__(self, value):
        qs = value['sheet'].store.profiles.filter(
            id=value['attendant'].id
        )
        if not qs.exists():
            message = _('Profile for attendant is invalid.')
            raise serializers.ValidationError(message)


class AcceptAccountableValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        qs = value['sheet'].customer.profiles.filter(
            id=request.user.profile.id
        )
        if not qs.exists():
            message = _('Profile for accept is invalid.')
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
            if k in tran.payload.keys()
        }
        data.update({'store': tran.store})
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
