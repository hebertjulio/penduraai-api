from django.db.models import Sum, Case, When, F, DecimalField

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Record


class OweToYourselfValidator:

    def __call__(self, data):
        creditor = data['creditor']
        debtor = data['debtor']
        if creditor.id == debtor.id:
            message = _('you can\'t owe to yourself.')
            raise serializers.ValidationError(message)


class IsCustomerValidator:

    def __call__(self, data):
        creditor = data['creditor']
        debtor = data['debtor']
        customer = creditor.customers_creditor.filter(debtor=debtor)
        if not customer.exists():
            message = _('You aren\'t a costumer.')
            raise serializers.ValidationError(message)


class CustomerFromYourselfValidator:

    def __call__(self, data):
        creditor = data['creditor']
        debtor = data['debtor']
        if creditor.id == debtor.id:
            message = _('You can\'t customer from yourself.')
            raise serializers.ValidationError(message)


class BalanceWhenPaymentValidator:

    def __call__(self, data):
        if data['operation'] == Record.OPERATION.debt:
            return
        value = data['value']
        creditor = data['creditor']
        debtor = data['debtor']
        balance = BalanceWhenPaymentValidator.get_balance(creditor, debtor)
        balance_final = balance + value
        if balance_final > 0:
            message = _('Balance cannot be positive.')
            raise serializers.ValidationError(message)

    @staticmethod
    def get_balance(creditor, debtor):
        try:
            payment_sum = Sum(Case(When(
                operation='payment', then=F('value')), default=0,
                output_field=DecimalField()))
            debt_sum = Sum(Case(When(
                operation='debt', then=F('value')), default=0,
                output_field=DecimalField()))
            qs = Record.objects.values('creditor')
            qs = qs.annotate(payment_sum=payment_sum, debt_sum=debt_sum)
            obj = qs.get(creditor=creditor, debtor=debtor)
            balance = obj['payment_sum'] - obj['debt_sum']
        except Record.DoesNotExist:
            balance = 0
        return balance
