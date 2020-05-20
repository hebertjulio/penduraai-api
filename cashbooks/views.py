from django.db.models import Q

from rest_framework import generics

from .models import Transaction, Whitelist
from .serializers import (
    TransactionSerializer, CreditorSerializar, DebtorSerializar,
    WhitelistSerializer)


class TransactionListView(generics.ListCreateAPIView):

    serializer_class = TransactionSerializer
    filterset_fields = (
        'creditor', 'debtor',
    )

    def get_queryset(self):
        user = self.request.user
        qs = Transaction.objects.filter(Q(creditor=user) | Q(debtor=user))
        return qs


class CreditorListView(generics.ListAPIView):

    serializer_class = CreditorSerializar

    def get_queryset(self):
        user = self.request.user
        qs = Transaction.objects.select_related().filter(debtor=user)
        return qs


class DebtorListView(generics.ListAPIView):

    serializer_class = DebtorSerializar

    def get_queryset(self):
        user = self.request.user
        qs = Transaction.objects.select_related().filter(creditor=user)
        return qs


class WhitelistListView(generics.ListCreateAPIView):

    serializer_class = WhitelistSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Whitelist.objects.filter(owner=user)
        return qs


class WhitelistDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = WhitelistSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Whitelist.objects.filter(owner=user)
        return qs
