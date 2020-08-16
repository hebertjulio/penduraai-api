from rest_framework.permissions import BasePermission

from .models import Profile


class HasProfile(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        profile = getattr(request, 'profile', None)
        return bool(profile and profile.user.id == user.id)


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        profile = getattr(request, 'profile', None)
        return bool(profile and profile.role == Profile.ROLE.owner)


class IsManager(IsOwner):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            profile = getattr(request, 'profile', None)
            return bool(profile and profile.role == Profile.ROLE.manager)
        return has_permission


class IsAttendant(IsManager):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            profile = getattr(request, 'profile', None)
            return bool(profile and profile.role == Profile.ROLE.attendant)
        return has_permission


class IsGuest(IsAttendant):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            profile = getattr(request, 'profile', None)
            return bool(profile and profile.role == Profile.ROLE.guest)
        return has_permission
