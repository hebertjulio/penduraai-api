from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class CustomerOfMerchantValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        if value.customer.id != request.user.id:
            message = _('You aren\'t customer of merchant.')
            raise serializers.ValidationError(message)


class CustomerOfYourselfValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        if value.id == user.id:
            message = _('You can\'t customer of yourself.')
            raise serializers.ValidationError(message)


class AlreadyCustomerOfMerchantValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        qs = user.customersheets.filter(merchant=value)
        if qs.exists():
            message = _('You are already customer of merchant.')
            raise serializers.ValidationError(message)


class EmployeeOfMerchantValidator:

    def __call__(self, value):
        if 'merchant' in value and 'attendant' in value:
            attendant = value['attendant']
            merchant = value['merchant']
            qs = merchant.userprofiles.filter(id=attendant.id, is_active=True)
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
        if not request.profile.is_owner:
            merchant = value['merchant']
            qs = merchant.merchantsheets.filter(
                customer=request.user, buyers=request.profile)
            if not qs.exists():
                message = _('You cannot buy from this merchant.')
                raise serializers.ValidationError(message)
