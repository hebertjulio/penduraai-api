from django.db.models import Q

from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

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


class RecordStrikethroughView(APIView):

    def get_object(self, pk, user):
        try:
            user = self.request.user
            obj = Record.objects.get(pk=pk, creditor=user)
            return obj
        except Record.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        user = self.request.user
        obj = self.get_object(pk, user)
        obj.strikethrough = True
        serializer = RecordSerializer(obj)
        return Response(serializer.data)

    def delete(self, request, pk):
        user = self.request.user
        obj = self.get_object(pk, user)
        obj.strikethrough = False
        serializer = RecordSerializer(obj)
        return Response(serializer.data)


class CustomerListView(generics.CreateAPIView):

    serializer_class = CustomerSerializer


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = CustomerSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Customer.objects.filter(creditor=user)
        return qs


class CreditorListView(generics.ListAPIView):

    serializer_class = CreditorSerializar
    filter_backends = [SearchFilter]
    search_fields = ['creditor__name']

    def get_queryset(self):
        user = self.request.user
        values = ('creditor__id', 'creditor__name', 'balance')
        qs = Customer.objects.creditors(user)
        qs = qs.order_by('creditor__name')
        qs = qs.values(*values)
        return qs


class DebtorListView(generics.ListAPIView):

    serializer_class = DebtorSerializar
    filter_backends = [SearchFilter]
    search_fields = ['debtor__name']

    def get_queryset(self):
        user = self.request.user
        values = ('debtor__id', 'debtor__name', 'balance')
        qs = qs = Customer.objects.debtors(user)
        qs = qs.order_by('debtor__name')
        qs = qs.values(*values)
        return qs
