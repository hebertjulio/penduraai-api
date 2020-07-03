from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class IsMerchantCustomerValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        qs = request.user.customersheets.filter(merchant=value, is_active=True)
        if not qs.exists():
            message = _('You aren\'t customer of this merchant.')
            raise serializers.ValidationError(message)


class CustomerOfYourselfValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        if value.id == user.id:
            message = _('You can\'t customer of your merchant.')
            raise serializers.ValidationError(message)


class AlreadyAMerchantCustomerValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        qs = user.customersheets.filter(merchant=value)
        if qs.exists():
            message = _('You are already a customer of this merchant.')
            raise serializers.ValidationError(message)


class MerchantEmployeeValidator:

    def __call__(self, value):
        if 'merchant' in value and 'attendant' in value:
            merchant = value['merchant']
            qs = merchant.userprofiles.filter(
                id=value['attendant'].id, is_active=True)
            if not qs.exists():
                message = _('Attendant isn\'t merchant employee.')
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
        merchant = value['merchant']
        qs = merchant.merchantsheets.filter(
            customer=request.user, buyers=request.profile)
        if not qs.exists():
            message = _('You can\'t buy from this merchant.')
            raise serializers.ValidationError(message)
