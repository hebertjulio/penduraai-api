from django.db.models import Q, Sum, Case, When, F, DecimalField

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
        c = Sum(Case(When(operation='credit', then=F('value')),
                output_field=DecimalField(), default=0))
        d = Sum(Case(When(operation='debit', then=F('value')),
                output_field=DecimalField(), default=0))
        qs = Transaction.objects.annotate(credit_sum=c, debit_sum=d)
        qs = qs.select_related('creditor').filter(debtor=user)
        return qs


class DebtorListView(generics.ListAPIView):

    serializer_class = DebtorSerializar

    def get_queryset(self):
        user = self.request.user
        c = Sum(Case(When(operation='credit', then=F('value')),
                output_field=DecimalField(), default=0))
        d = Sum(Case(When(operation='debit', then=F('value')),
                output_field=DecimalField(), default=0))
        qs = Transaction.objects.annotate(credit_sum=c, debit_sum=d)
        qs = qs.select_related('debtor').filter(creditor=user)
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
