from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Record, Customer


class OweToYourselfValidator:

    def __call__(self, value):
        if value['creditor'].id == value['debtor'].id:
            message = _('you can\'t owe to yourself.')
            raise serializers.ValidationError(message)


class IsCustomerValidator:

    def __call__(self, value):
        qs = value['creditor'].customers_creditor.filter(
            debtor=value['debtor'])
        if not qs.exists():
            message = _('You aren\'t a costumer.')
            raise serializers.ValidationError(message)


class CustomerFromYourselfValidator:

    def __call__(self, value):
        if value['creditor'].id == value['debtor'].id:
            message = _('You can\'t customer from yourself.')
            raise serializers.ValidationError(message)


class PositiveBalanceValidator:

    def __call__(self, value):
        if value['operation'] == Record.OPERATION.debt:
            return
        balance = Customer.objects.balance(value['creditor'], value['debtor'])
        balance = balance + value['value']
        if balance > 0:
            message = _('Balance cannot be positive.')
            raise serializers.ValidationError(message)
