import json

from django.db.models import Q

from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Record, CustomerRecord
from .dictdb import Transaction
from .services import send_message
from .serializers import (
    RecordSerializer, CustomerRecordSerializer, CreditorDebtorSerializar,
    TransactionSerializer
)


class RecordListView(generics.ListCreateAPIView):

    serializer_class = RecordSerializer
    filterset_fields = [
        'customer_record__creditor_id',
        'customer_record__debtor_id',
    ]

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

    serializer_class = CreditorDebtorSerializar
    filter_backends = [SearchFilter]
    search_fields = ['user_name']

    def get_queryset(self):
        user = self.request.user
        qs = CustomerRecord.objects.creditors(user)
        return qs


class DebtorListView(generics.ListAPIView):

    serializer_class = CreditorDebtorSerializar
    filter_backends = [SearchFilter]
    search_fields = ['user_name']

    def get_queryset(self):
        user = self.request.user
        qs = CustomerRecord.objects.debtors(user)
        return qs


class TransactionListView(APIView):

    def post(self, request):  # skipcq
        context = {'request': request}
        serializer = TransactionSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class TransactionDetailView(APIView):

    def get(self, request, pk):  # skipcq
        tran = Transaction(pk)
        if not tran.exist():
            raise NotFound
        return Response(tran.data, status=HTTP_200_OK)


class TransactionRejectView(APIView):

    def put(self, request, pk):  # skipcq
        tran = Transaction(pk)
        if not tran.exist():
            raise NotFound
        tran.status = Transaction.STATUS.rejected
        tran.save()
        send_message(tran.id, json.dumps(tran.data))
        return Response(tran.data, status=HTTP_200_OK)
