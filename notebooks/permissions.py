from rest_framework.exceptions import NotAcceptable

from accounts.permissions import IsOwner

from .models import Record


class CanBuy(IsOwner):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if has_permission:
            return True

        transaction = request.transaction
        profile = request.profile

        if transaction is None:
            raise NotAcceptable

        data = transaction.get_data()

        if 'operation' in data:
            operation = data['operation']
            if operation == Record.OPERATION.credit:
                return True

        if 'store' in data:
            store = data['store']
            qs = profile.profilebuyers.select_related('sheet')
            qs = qs.filter(sheet__store=store)
            return bool(qs.exists())

        return False
