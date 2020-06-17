from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        profile = request.user.profile
        return bool(profile.is_owner)


class IsManager(IsOwner):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            profile = request.user.profile
            return bool(profile.is_manager)
        return has_permission


class IsAttendant(IsManager):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            profile = request.user.profile
            return bool(profile.is_attendant)
        return has_permission
