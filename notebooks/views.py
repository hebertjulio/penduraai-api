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
    RecordTransactionSerializer, CustomerRecordTransactionSerializer
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
            Q(customer_record__creditor=user) |
            Q(customer_record__debtor=user)
        )
        qs = qs.order_by('-created')
        return qs


class RecordDetailView(generics.RetrieveAPIView):

    lookup_field = 'pk'
    serializer_class = RecordSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Record.objects.filter(
            Q(customer_record__creditor=user) |
            Q(customer_record__debtor=user)
        )
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

    def get(self, request, pk):  # skipcq
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


class DebtorCreditorListView(generics.ListAPIView):

    lookup_field = 'switch'
    serializer_class = CreditorDebtorSerializar
    filter_backends = [SearchFilter]
    search_fields = ['user_name']

    def get_queryset(self):
        switch = self.kwargs['switch']
        user = self.request.user
        if switch == 'debtors':
            return CustomerRecord.objects.debtors(user)
        return CustomerRecord.objects.creditors(user)


class TransactionListView(APIView):

    def post(self, request, switch):  # skipcq
        context = {'request': request}
        params = {'data': request.data, 'context': context}
        if switch == 'new-record':
            params['data'].update({
                'action': Transaction.ACTION.new_record
            })
            serializer = RecordTransactionSerializer(**params)
        else:
            params['data'].update({
                'action': Transaction.ACTION.new_customer_record
            })
            serializer = CustomerRecordTransactionSerializer(**params)
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
