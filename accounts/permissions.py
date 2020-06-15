from rest_framework.permissions import BasePermission

from .models import Profile


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        profile = request.user.profile
        return bool(
            profile is not None and profile.role == Profile.ROLE.owner
        )


class IsAdmin(IsOwner):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            profile = request.user.profile
            return bool(
                profile is not None and profile.role == Profile.ROLE.admin
            )
        return has_permission


class CanAttend(IsAdmin):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            profile = request.user.profile
            return bool(
                profile is not None and profile.can_attend
            )
        return has_permission


class CanBuy(IsAdmin):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            profile = request.user.profile
            return bool(
                profile is not None and profile.can_buy
            )
        return has_permission
