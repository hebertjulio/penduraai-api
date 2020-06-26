from rest_framework.permissions import BasePermission

from .models import Profile


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        profile = request.user.profile
        return bool(
            profile and profile.role == Profile.ROLE.owner)


class IsManager(IsOwner):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            profile = request.user.profile
            return bool(
                profile and profile.role == Profile.ROLE.manager)
        return has_permission


class IsAttendant(IsManager):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            profile = request.user.profile
            return bool(
                profile and profile.role == Profile.ROLE.attendant)
        return has_permission


class IsGuest(IsManager):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            profile = request.user.profile
            return bool(
                profile and profile.role == Profile.ROLE.guest)
        return has_permission
