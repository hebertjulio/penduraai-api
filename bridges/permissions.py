from rest_framework.permissions import BasePermission

from .models import Transaction


class HasTransaction(BasePermission):

    def has_permission(self, request, view):
        transaction = getattr(request, 'transaction', None)
        if transaction:
            return bool(
                transaction.status == Transaction.STATUS.unused
                and not transaction.expired)
        return False
