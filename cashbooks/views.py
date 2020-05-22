from django.db.models import Q, Sum, Case, When, F, DecimalField

from rest_framework import generics

from .models import Record, Whitelist

from .serializers import (
    RecordSerializer, CreditorSerializar, DebtorSerializar,
    WhitelistSerializer
)


class RecordListView(generics.ListCreateAPIView):

    serializer_class = RecordSerializer
    filterset_fields = (
        'creditor', 'debtor',
    )

    def get_queryset(self):
        user = self.request.user
        qs = Record.objects.filter(Q(creditor=user) | Q(debtor=user))
        return qs


class CreditorListView(generics.ListAPIView):

    serializer_class = CreditorSerializar

    def get_queryset(self):
        credit_sum = Sum(Case(When(
            operation='credit', then=F('value')), output_field=DecimalField(),
            default=0))
        debit_sum = Sum(Case(When(
            operation='debit', then=F('value')), output_field=DecimalField(),
            default=0))
        user = self.request.user
        qs = Record.objects.values('creditor__id', 'creditor__name')
        qs = qs.annotate(credit_sum=credit_sum, debit_sum=debit_sum)
        qs = qs.filter(debtor=user)
        return qs


class DebtorListView(generics.ListAPIView):

    serializer_class = DebtorSerializar

    def get_queryset(self):
        credit_sum = Sum(Case(When(
            operation='credit', then=F('value')), output_field=DecimalField(),
            default=0))
        debit_sum = Sum(Case(When(
            operation='debit', then=F('value')), output_field=DecimalField(),
            default=0))
        user = self.request.user
        qs = Record.objects.values('debtor__id', 'debtor__name')
        qs = qs.annotate(credit_sum=credit_sum, debit_sum=debit_sum)
        qs = qs.filter(creditor=user)
        return qs


class WhitelistListView(generics.ListCreateAPIView):

    serializer_class = WhitelistSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Whitelist.objects.filter(creditor=user)
        return qs


class WhitelistDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = WhitelistSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Whitelist.objects.filter(creditor=user)
        return qs
