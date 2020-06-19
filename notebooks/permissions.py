from accounts.permissions import IsOwner


from .models import Record


class CanBuy(IsOwner):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        profile = request.user.profile
        if profile and not has_permission:
            # Ignore buy permission if payment
            if 'operation' in request.data:
                operation = request.data['operation']
                if operation == Record.OPERATION.credit:
                    return True
            if 'store' in request.data:
                store = request.data['store']
                qs = profile.profilebuyers.select_related('sheet')
                qs = qs.filter(sheet__store=store)
                return qs.exists()
        return has_permission
