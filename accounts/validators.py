from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class AccountablePINUniqueTogetherValidator:

    def __call__(self, value):
        qs = value['accountable'].profiles.filter(
            pin=value['pin'], is_active=True)
        if qs.exists():
            message = _('PIN must be unique by account.')
            raise serializers.ValidationError(message)
