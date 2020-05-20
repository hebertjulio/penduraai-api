from django.db.models import Q

from rest_framework import generics

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionListView(generics.ListCreateAPIView):

    serializer_class = TransactionSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Transaction.objects.filter(
            Q(creditor=user) | Q(debtor=user), status=Transaction.STATUS.done)
        return qs
