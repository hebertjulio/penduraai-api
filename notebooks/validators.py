from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class EmployeeOfMerchantValidator:

    def __call__(self, value):
        if 'merchant' in value and 'attendant' in value:
            qs = value['merchant'].userprofiles.filter(
                id=value['attendant'].id, is_active=True)
            if not qs.exists():
                message = _('You aren\'t employee of merchant.')
                raise serializers.ValidationError(message)


class SheetBelongCustomerValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        qs = user.customersheets.filter(id=value.id)
        if not qs.exists():
            message = _('This sheet does not belong to you.')
            raise serializers.ValidationError(message)


class ProfileCanBuyValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        if not request.user.profile.is_owner:
            qs = value['merchant'].merchantsheets.filter(
                customer=request.user, buyers=request.user.profile)
            if not qs.exists():
                message = _('You cannot buy from this merchant.')
                raise serializers.ValidationError(message)
