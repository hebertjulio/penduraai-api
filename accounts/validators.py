from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class DebtorAccountable:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        debtor_id = request.user.id
        if value.accountable.id != debtor_id:
            message = _('debtor isn\'t accountable of buyer.')
            raise serializers.ValidationError(message)


class CreditorAccountable:

    requires_context = True

    def __call__(self, value, serializer_field):
        parent = serializer_field.parent
        creditor_id = int(parent.initial_data['creditor'])
        if value.accountable.id != creditor_id:
            message = _('creditor isn\'t accountable of seller.')
            raise serializers.ValidationError(message)
