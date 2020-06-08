from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import BasePermission

from .models import Profile


class IsOwner(BasePermission):
    message = _('Profile does not have privileges to perform this action.')

    def has_permission(self, request, view):
        profile = request.user.profile
        return bool(
            profile is not None
            and profile.role == Profile.ROLE.owner
        )


class IsManager(IsOwner):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            profile = request.user.profile
            return bool(
                profile is not None
                and profile.role == Profile.ROLE.manager
            )
        return has_permission


class IsSeller(IsManager):
    roles = [
        Profile.ROLE.seller, Profile.ROLE.both
    ]

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            profile = request.user.profile
            return bool(
                profile is not None
                and profile.role in self.roles
            )
        return has_permission


class IsBuyer(IsManager):
    roles = [
        Profile.ROLE.buyer, Profile.ROLE.both
    ]

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            profile = request.user.profile
            return bool(
                profile is not None
                and profile.role in self.roles
            )
        return has_permission
