from rest_framework.permissions import BasePermission

from .models import Profile


class ProfileSalePermission(BasePermission):
    message = 'Sale not allowed.'

    roles = [
        Profile.ROLE.owner, Profile.ROLE.manager,
        Profile.ROLE.seller, Profile.ROLE.both
    ]

    def has_permission(self, request, view):
        profile = request.profile
        return bool(
            profile is not None
            and profile.role in self.roles
        )


class ProfileShopPermission(BasePermission):
    message = 'Shop not allowed.'

    roles = [
        Profile.ROLE.owner, Profile.ROLE.manager,
        Profile.ROLE.buyer, Profile.ROLE.both
    ]

    def has_permission(self, request, view):
        profile = request.profile
        return bool(
            profile is not None
            and profile.role in self.roles
        )


class ProfileAddCustomerPermission(BasePermission):
    message = 'Add customer not allowed.'

    roles = [
        Profile.ROLE.owner, Profile.ROLE.manager
    ]

    def has_permission(self, request, view):
        profile = request.profile
        return bool(
            profile is not None
            and profile.role in self.roles
        )
