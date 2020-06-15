from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        profile = request.user.profile
        return bool(
            profile is not None and profile.is_owner)


class IsManager(IsOwner):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            profile = request.user.profile
            return bool(
                profile is not None and profile.is_manager)
        return has_permission


class IsAttendant(IsOwner):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            profile = request.user.profile
            return bool(
                profile is not None and profile.is_attendant)
        return has_permission
