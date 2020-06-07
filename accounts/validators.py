from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


from .models import Profile


class CanSaleOrReceivePaymentValidator:

    roles = [
        Profile.ROLE.owner, Profile.ROLE.manager,
        Profile.ROLE.seller, Profile.ROLE.both,
    ]

    def __call__(self, value):
        print(value)
        if value.role not in self.roles:
            message = _(
                'You do not have privileges to make '
                'sales or receive payments.')
            raise serializers.ValidationError(message)


class CanShopValidator:

    roles = [
        Profile.ROLE.owner, Profile.ROLE.manager,
        Profile.ROLE.buyer, Profile.ROLE.both,
    ]

    def __call__(self, value):
        if value.role not in self.roles:
            message = _('You have no privileges to shop.')
            raise serializers.ValidationError(message)


class CanAddNewCustomerValidator:

    roles = [
        Profile.ROLE.owner, Profile.ROLE.manager
    ]

    def __call__(self, value):
        if value.role not in self.roles:
            message = _('You have no privileges add new customer.')
            raise serializers.ValidationError(message)
