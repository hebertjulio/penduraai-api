from rest_framework import generics

from .serializers import TransactionSerializer
from .models import Transaction


class TransactionDetailView(generics.RetrieveAPIView):

    lookup_field = 'pk'
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class TransactionRejectView(generics.UpdateAPIView):

    lookup_field = 'pk'
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
