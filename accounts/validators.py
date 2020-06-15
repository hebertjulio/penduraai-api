from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class UserPINUniqueTogetherValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        if 'pin' in value:
            request = serializer_field.context['request']
            user = request.user
            qs = user.userprofiles.filter(pin=value['pin'], is_active=True)
            if qs.exists():
                message = _('PIN must be unique by user.')
                raise serializers.ValidationError(message)


class ProfileBelongUserValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        qs = user.userprofiles.filter(id=value.id)
        if not qs.exists():
            message = _('This profile does not belong to you.')
            raise serializers.ValidationError(message)
