import json

from django.db.models import Q

from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.permissions import CanBuy, CanSell, IsAdmin

from .models import Record, Sheet
from .dictdb import Transaction
from .services import send_message

from .serializers import (
    RecordSerializer, SheetSerializer, BalanceSerializar,
    TransactionSerializer
)


class RecordListView(generics.ListCreateAPIView):

    serializer_class = RecordSerializer
    filterset_fields = [
        'sheet__store',
        'sheet__customer',
    ]

    def get_queryset(self):
        user = self.request.user
        profile = user.profile
        where = (Q(sheet__store=user) | Q(sheet__customer=user))
        if not profile.is_admin():
            where = where & (Q(seller=profile) | Q(buyer=profile))
        qs = Record.objects.select_related('sheet', 'seller', 'buyer')
        qs = qs.filter(where)
        qs = qs.order_by('-created')
        return qs

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method == 'POST':
            permissions += [CanBuy()]
        return permissions


class RecordDetailView(generics.RetrieveDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = RecordSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method == 'DELETE':
            permissions += [IsAdmin()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        if self.request.method == 'DELETE':
            where = Q(sheet__store=user)
        else:
            where = Q(sheet__store=user) | Q(sheet__customer=user)
        qs = Record.objects.select_related(
            'sheet', 'sheet__customer', 'sheet__store', 'seller', 'buyer')
        qs = qs.filter(where)
        return qs

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
        return instance


class SheetListView(generics.CreateAPIView):

    serializer_class = SheetSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [IsAdmin()]
        return permissions


class SheetDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = SheetSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permissions += [IsAdmin()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        qs = Sheet.objects.filter(Q(store=user) | Q(customer=user))
        return qs


class SheetDetailByStoreView(APIView):

    def get(self, request, pk):  # skipcq
        user = request.user
        try:
            obj = user.customer.get(store_id=pk, authorized=True)
            serializer = SheetSerializer(obj)
            response = Response(serializer.data)
            return response
        except Sheet.DoesNotExist:
            raise NotFound


class BalanceListByStoreView(generics.ListAPIView):

    serializer_class = BalanceSerializar
    filter_backends = [SearchFilter]
    search_fields = ['user_name']

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [CanBuy()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        qs = Sheet.objects.balance_list_by_store(user)
        return qs


class BalanceListByCustomerView(generics.ListAPIView):

    serializer_class = BalanceSerializar
    filter_backends = [SearchFilter]
    search_fields = ['user_name']

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [CanSell()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        qs = Sheet.objects.balance_list_by_customer(user)
        return qs


class TransactionNewRecordView(APIView):

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [CanSell()]
        return permissions

    def post(self, request):  # skipcq
        context = {'request': request}
        request.data.update({'action': Transaction.ACTION.new_record})
        serializer = TransactionSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class TransactionNewSheetView(APIView):

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [IsAdmin()]
        return permissions

    def post(self, request):  # skipcq
        context = {'request': request}
        request.data.update({'action': Transaction.ACTION.new_sheet})
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
