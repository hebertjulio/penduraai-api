from rest_framework.permissions import BasePermission


class HasTransaction(BasePermission):

    def has_permission(self, request, view):
        transaction = getattr(request, 'transaction', None)
        return bool(transaction is not None)
