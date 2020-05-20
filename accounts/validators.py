from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class ProfileOf:

    requires_context = True

    def __call__(self, profile, serializer_field):
        request = serializer_field.parent.context['request']
        field_name = serializer_field.field_name

        accountable_fields = {'requester': 'creditor', 'subscriber': 'debtor'}
        accountable_field = accountable_fields[field_name]

        if field_name == 'requester':
            user_id = int(request.data.get('creditor', 0))
        else:
            user_id = request.user.id

        if profile.accountable_id != user_id:
            message = _(
                '%s is not accountable of %s.' % (
                    accountable_field.title(), field_name))
            raise serializers.ValidationError(message)
