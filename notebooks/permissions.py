from accounts.permissions import IsOwner


from .models import Record


class CanBuy(IsOwner):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            if 'store' in request.data and 'operation' in request.data:
                operation = request.data['operation']
                if operation == Record.OPERATION.credit:
                    return True  # payment
                store = request.data['store']
                profile = request.user.profile
                qs = profile.profilebuyers.select_related('sheet')
                qs = qs.filter(sheet__store=store)
                return qs.exists()
        return has_permission
