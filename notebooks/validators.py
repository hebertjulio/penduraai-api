from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class CreditorAndDebtorSameUserValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        if value['creditor'].id == request.user.id:
            message = _('you can\'t owe to yourself')
            raise serializers.ValidationError(message)


class IsCustomerValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        customer = value['creditor'].customers_creditor.filter(
            debtor_id=request.user.id)
        if not customer.exists():
            message = _('you aren\'t a costumer.')
            raise serializers.ValidationError(message)
