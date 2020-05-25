import json

from django.db.models import Q, Sum, Case, When, F, DecimalField

from rest_framework import generics

from .models import Record, Customer
from .storages import Transaction

from .serializers import (
    RecordSerializer, CreditorSerializar, DebtorSerializar,
    CustomerSerializer
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

    def perform_create(self, serializer):
        tran = Transaction(self.request.data['transaction'])
        data = json.loads(tran.data)
        data.update({'debtor': self.request.user})
        serializer.save(**data)


class CreditorListView(generics.ListAPIView):

    serializer_class = CreditorSerializar

    def get_queryset(self):
        payment_sum = Sum(Case(When(
            operation='payment', then=F('value')), output_field=DecimalField(),
            default=0))
        debt_sum = Sum(Case(When(
            operation='debt', then=F('value')), output_field=DecimalField(),
            default=0))
        user = self.request.user
        qs = Record.objects.values('creditor__id', 'creditor__name')
        qs = qs.annotate(payment_sum=payment_sum, debt_sum=debt_sum)
        qs = qs.filter(debtor=user)
        return qs


class DebtorListView(generics.ListAPIView):

    serializer_class = DebtorSerializar

    def get_queryset(self):
        payment_sum = Sum(Case(When(
            operation='payment', then=F('value')), output_field=DecimalField(),
            default=0))
        debt_sum = Sum(Case(When(
            operation='debt', then=F('value')), output_field=DecimalField(),
            default=0))
        user = self.request.user
        qs = Record.objects.values('debtor__id', 'debtor__name')
        qs = qs.annotate(payment_sum=payment_sum, debt_sum=debt_sum)
        qs = qs.filter(creditor=user)
        return qs


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
