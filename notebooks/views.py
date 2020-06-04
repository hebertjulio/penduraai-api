from django.db.models import Q

from rest_framework import generics
from rest_framework import filters

from .models import Record, Customer

from .serializers import (
    RecordSerializer, CustomerSerializer, CreditorSerializar,
    DebtorSerializar)


class RecordListView(generics.ListCreateAPIView):

    serializer_class = RecordSerializer
    filterset_fields = ['creditor', 'debtor']

    def get_queryset(self):
        user = self.request.user
        qs = Record.objects.filter(Q(creditor=user) | Q(debtor=user))
        qs = qs.order_by('-created')
        return qs


class RecordDetailView(generics.RetrieveAPIView):

    lookup_field = 'pk'
    serializer_class = RecordSerializer
    queryset = Record.objects.all()


class CustomerListView(generics.ListCreateAPIView):

    serializer_class = CustomerSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Customer.objects.filter(creditor=user)
        return qs


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = CustomerSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Customer.objects.filter(creditor=user)
        return qs


class CreditorListView(generics.ListAPIView):

    serializer_class = CreditorSerializar
    filter_backends = [filters.SearchFilter]
    search_fields = ['creditor__name']

    def get_queryset(self):
        user = self.request.user
        values = ('creditor__id', 'creditor__name', 'balance')
        qs = Customer.objects.creditors(user)
        qs = qs.values(*values)
        return qs


class DebtorListView(generics.ListAPIView):

    serializer_class = DebtorSerializar
    filter_backends = [filters.SearchFilter]
    search_fields = ['debtor__name']

    def get_queryset(self):
        user = self.request.user
        values = ('debtor__id', 'debtor__name', 'balance')
        qs = qs = Customer.objects.debtors(user)
        qs = qs.values(*values)
        return qs
