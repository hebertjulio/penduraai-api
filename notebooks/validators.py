from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Record, Customer


class OweToYourselfValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        if value['creditor'].id == user.id:
            message = _('you can\'t owe to yourself.')
            raise serializers.ValidationError(message)


class IsCustomerValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        qs = value['creditor'].customers_creditor.filter(debtor=user)
        if not qs.exists():
            message = _('You aren\'t a costumer.')
            raise serializers.ValidationError(message)


class CustomerFromYourselfValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        if value['creditor'].id == user.id:
            message = _('You can\'t customer from yourself.')
            raise serializers.ValidationError(message)


class PositiveBalanceValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        if value['operation'] == Record.OPERATION.debt:
            return
        request = serializer_field.context['request']
        user = request.user
        balance = Customer.objects.balance(value['creditor'], user)
        balance = balance + value['value']
        if balance > 0:
            message = _('Balance cannot be positive.')
            raise serializers.ValidationError(message)


class AlreadyACustomerValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        qs = user.customers_debtor.filter(creditor=value['creditor'])
        if qs.exists():
            message = _('You are already a customer.')
            raise serializers.ValidationError(message)
