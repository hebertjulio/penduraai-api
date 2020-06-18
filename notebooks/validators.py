from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class IsStoreCustomerValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        qs = request.user.customersheets.filter(store=value, is_active=True)
        if not qs.exists():
            message = _('You aren\'t customer of this store.')
            raise serializers.ValidationError(message)


class CustomerOfYourselfValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        if value.id == user.id:
            message = _('You can\'t customer of your store.')
            raise serializers.ValidationError(message)


class AlreadyAStoreCustomerValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        qs = user.customersheets.filter(store=value)
        if qs.exists():
            message = _('You are already a customer of this store.')
            raise serializers.ValidationError(message)


class StoreEmployeeValidator:

    def __call__(self, value):
        if 'store' in value and 'attendant' in value:
            user = value['store']
            qs = user.userprofiles.filter(
                id=value['attendant'].id, is_active=True)
            if not qs.exists():
                message = _('Attendant isn\'t store employee.')
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
