from django.db.models import Q

from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Record, CustomerRecord

from .serializers import (
    RecordSerializer, CustomerRecordSerializer, CreditorSerializar,
    DebtorSerializar)


class RecordListView(generics.ListCreateAPIView):

    serializer_class = RecordSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Record.objects.filter(
            Q(customer_record__creditor=user) | Q(customer_record__debtor=user)
        )
        qs = qs.order_by('-created')
        return qs


class RecordDetailView(generics.RetrieveAPIView):

    lookup_field = 'pk'
    serializer_class = RecordSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Record.objects.filter(Q(creditor=user) | Q(debtor=user))
        return qs


class RecordStrikethroughView(APIView):

    def patch(self, request, pk):
        try:
            user = self.request.user
            obj = Record.objects.get(pk=pk, creditor=user)
            obj.strikethrough = True
            obj.save()
            serializer = RecordSerializer(obj)
            return Response(serializer.data)
        except Record.DoesNotExist:
            raise NotFound


class CustomerRecordListView(generics.CreateAPIView):

    serializer_class = CustomerRecordSerializer


class DebtorCustomerRecordView(APIView):

    def get(self, request, pk):
        try:
            user = request.user
            obj = user.as_debtor.get(creditor_id=pk)
            serializer = CustomerRecordSerializer(obj)
            return Response(serializer.data)
        except CustomerRecord.DoesNotExist:
            raise NotFound


class CustomerRecordDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = CustomerRecordSerializer

    def get_queryset(self):
        user = self.request.user
        qs = CustomerRecord.objects.filter(creditor=user)
        return qs


class CreditorListView(generics.ListAPIView):

    serializer_class = CreditorSerializar
    filter_backends = [SearchFilter]
    search_fields = ['creditor__name']

    def get_queryset(self):
        user = self.request.user
        values = ('creditor__id', 'creditor__name', 'balance')
        qs = CustomerRecord.objects.creditors(user)
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
        qs = qs = CustomerRecord.objects.debtors(user)
        qs = qs.order_by('debtor__name')
        qs = qs.values(*values)
        return qs
