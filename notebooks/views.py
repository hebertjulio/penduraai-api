import json

from django.db.models import Q

from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.permissions import IsManager, IsAttendant

from .permissions import CanBuy
from .models import Record, Sheet, Buyer
from .dictdb import Transaction
from .services import send_message
from .serializers import (
    RecordSerializer, SheetSerializer, BalanceSerializar,
    TransactionSerializer, BuyerSerializer
)


class RecordListView(generics.ListCreateAPIView):

    serializer_class = RecordSerializer
    filterset_fields = [
        'sheet__store',
        'sheet__customer',
    ]

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method == 'POST':
            permissions += [CanBuy()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        profile = user.profile
        if profile.is_owner:
            where = Q(sheet__store=user) | Q(sheet__customer=user)
        elif profile.is_attendant or profile.is_manager:
            where = Q(sheet__store=user)
        else:
            where = Q(sheet__customer=user) & Q(signature=profile)
        qs = Record.objects.select_related('sheet', 'attendant', 'signature')
        qs = qs.filter(where)
        qs = qs.order_by('-created')
        return qs


class RecordDetailView(generics.RetrieveDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = RecordSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method == 'DELETE':
            permissions += [IsManager()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        where = Q(sheet__store=user)
        if self.request.method == 'GET':
            where = where | Q(sheet__customer=user)
        qs = Record.objects.select_related(
            'sheet', 'sheet__customer', 'sheet__store',
            'attendant', 'signature')
        qs = qs.filter(where)
        return qs

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class SheetListView(generics.CreateAPIView):

    serializer_class = SheetSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [IsManager()]
        return permissions


class SheetDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = SheetSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permissions += [IsManager()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        qs = Sheet.objects.select_related('customer', 'store')
        qs = qs.filter(store=user)
        qs = qs.order_by('customer__name')
        return qs


class BuyerListView(generics.ListCreateAPIView):

    serializer_class = BuyerSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [IsManager()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        qs = Buyer.objects.select_related('sheet', 'profile')
        qs = qs.filter(profile__user=user)
        qs = qs.order_by('profile__name')
        return qs


class BuyerDetailView(generics.DestroyAPIView):

    serializer_class = BuyerSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [IsManager()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        qs = Buyer.objects.filter(profile__user=user)
        return qs


class BalanceListByStoreView(generics.ListAPIView):

    serializer_class = BalanceSerializar

    filter_backends = [
        SearchFilter
    ]
    search_fields = [
        'user_name'
    ]

    def get_queryset(self):
        user = self.request.user
        profile = user.profile
        qs = Sheet.objects.balance_list_by_store(user, profile)
        return qs


class BalanceListByCustomerView(generics.ListAPIView):

    serializer_class = BalanceSerializar

    filter_backends = [
        SearchFilter
    ]
    search_fields = [
        'user_name'
    ]

    def get_queryset(self):
        user = self.request.user
        profile = user.profile
        qs = Sheet.objects.balance_list_by_customer(user, profile)
        return qs


class TransactionNewRecordView(APIView):

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [IsAttendant()]
        return permissions

    def post(self, request, version):  # skipcq
        context = {'request': request}
        request.data.update({'action': Transaction.ACTION.new_record})
        serializer = TransactionSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class TransactionNewSheetView(APIView):

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [IsManager()]
        return permissions

    def post(self, request, version):  # skipcq
        context = {'request': request}
        request.data.update({'action': Transaction.ACTION.new_sheet})
        serializer = TransactionSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class TransactionDetailView(APIView):

    def get(self, request, version, pk):  # skipcq
        tran = Transaction(pk)
        if not tran.exist():
            raise NotFound
        return Response(tran.data, status=HTTP_200_OK)


class TransactionRejectView(APIView):

    def put(self, request, version, pk):  # skipcq
        tran = Transaction(pk)
        if not tran.exist():
            raise NotFound
        tran.status = Transaction.STATUS.rejected
        tran.save()
        send_message(tran.id, json.dumps(tran.data))
        return Response(tran.data, status=HTTP_200_OK)
