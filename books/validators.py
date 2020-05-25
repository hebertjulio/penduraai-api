import json

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from broker.dictdb import Storage


class CreditorAndDebtorSameUserValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        stg = Storage(request.data['id'])
        data = json.loads(stg.record)
        if int(data['creditor_id']) == request.user.id:
            message = _('creditor and debtor are the same user.')
            raise serializers.ValidationError(message)
