from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class CreditorAndDebtorSameUserValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        if value['creditor'].id == request.user.id:
            message = _('creditor and debtor are the same user.')
            raise serializers.ValidationError(message)
