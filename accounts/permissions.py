from rest_framework.permissions import BasePermission

from .models import Profile


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        profile = request.profile
        return bool(profile and profile.role == Profile.ROLE.owner)


class IsManager(IsOwner):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if has_permission:
            return True
        profile = request.profile
        return bool(profile and profile.role == Profile.ROLE.manager)


class IsAttendant(IsManager):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if has_permission:
            return True
        profile = request.profile
        return bool(profile and profile.role == Profile.ROLE.attendant)


class IsGuest(IsAttendant):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if has_permission:
            return True
        profile = request.profile
        return bool(profile and profile.role == Profile.ROLE.guest)
