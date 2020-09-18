from rest_framework import generics

from rest_framework_api_key.permissions import HasAPIKey

from .serializers import TransactionReadSerializer
from .db import Transaction


class TransactionDetailView(generics.RetrieveDestroyAPIView):

    serializer_class = TransactionReadSerializer
    lookup_url_kwarg = 'transaction_id'

    permission_classes = [
        HasAPIKey
    ]

    def get_object(self):
        transaction_id = self.kwargs[self.lookup_url_kwarg]
        transaction = Transaction(transaction_id)
        transaction.exist(raise_exception=True)
        return transaction

    def perform_destroy(self, instance):
        instance.delete()
