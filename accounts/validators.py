from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class DebtorAccountable:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        debtor_id = request.user.id
        if value.accountable.id != debtor_id:
            message = _('Accountable for buyer is invalid.')
            raise serializers.ValidationError(message)


class CreditorAccountable:

    requires_context = True

    def __call__(self, value, serializer_field):
        parent = serializer_field.parent
        creditor_id = int(parent.initial_data['creditor'])
        if value.accountable.id != creditor_id:
            message = _('Accountable for seller is invalid.')
            raise serializers.ValidationError(message)
