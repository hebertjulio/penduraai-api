from rest_framework.permissions import BasePermission

from .models import Profile


class IsAuthenticatedAndProfileIsOwner(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        profile = request.profile
        return bool(
            user and user.is_authenticated and
            profile and profile.role == Profile.ROLE.owner)


class IsAuthenticatedAndProfileIsManager(IsAuthenticatedAndProfileIsOwner):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            user = request.user
            profile = request.profile
            return bool(
                user and user.is_authenticated and
                profile and profile.role == Profile.ROLE.manager)
        return has_permission


class IsAuthenticatedAndProfileIsAttendant(IsAuthenticatedAndProfileIsManager):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            user = request.user
            profile = request.profile
            return bool(
                user and user.is_authenticated and
                profile and profile.role == Profile.ROLE.attendant)
        return has_permission


class IsAuthenticatedAndProfileIsGuest(IsAuthenticatedAndProfileIsAttendant):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            user = request.user
            profile = request.profile
            return bool(
                user and user.is_authenticated and
                profile and profile.role == Profile.ROLE.guest)
        return has_permission
