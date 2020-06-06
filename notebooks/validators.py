from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class IsCustomerRecordOwnerValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        if value.debtor.id != user.id:
            message = _('you aren\'t owner of this customer record.')
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
