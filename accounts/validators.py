from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Profile


class AccountablePINUniqueTogetherValidator:

    def __call__(self, value):
        qs = value['accountable'].profiles.filter(
            pin=value['pin'], is_active=True)
        if qs.exists():
            message = _('PIN must be unique by account.')
            raise serializers.ValidationError(message)


class RoleOwnerValidator:

    def __call__(self, value):
        if value == Profile.ROLE.owner:
            message = _('Owner role is not allowed.')
            raise serializers.ValidationError(message)
