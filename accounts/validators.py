from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Profile


class IsRoleOwnerValidator:

    def __call__(self, value):
        if value == Profile.ROLE.owner:
            message = _('Role "owner" not allowed.')
            raise serializers.ValidationError(message)
