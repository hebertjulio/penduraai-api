from accounts.permissions import IsOwner


from .models import Record


class CanBuy(IsOwner):

    @classmethod
    def get_store(cls, view):
        if hasattr(view, 'transaction'):
            obj = view.transaction
            data = obj.get_data()
            if 'store' in data.keys():
                return data['store']
        return None

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            # Ignore buy permission if payment
            if 'operation' in request.data:
                operation = request.data['operation']
                if operation == Record.OPERATION.credit:
                    return True
            store = self.get_store(view)
            if store is not None:
                profile = request.user.profile
                qs = profile.profilebuyers.select_related('sheet')
                qs = qs.filter(sheet__store=store)
                return qs.exists()
        return has_permission
