from django.db.models import Q

from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from accounts.permissions import IsManager, IsAttendant, IsGuest

from bridges.decorators import use_transaction

from .permissions import CanBuy
from .models import Record, Sheet
from .serializers import (
    RecordRequestSerializer, RecordListSerializer, RecordDetailSerializer,
    SheetRequestSerializer, SheetListSerializer, SheetDetailSerializer,
    SheetBuyerAddSerializer, BalanceListSerializar
)


class RecordRequestView(generics.CreateAPIView):

    serializer_class = RecordRequestSerializer

    permission_classes = [
        IsAuthenticated, IsAttendant
    ]


class RecordListView(generics.ListCreateAPIView):

    serializer_class = RecordListSerializer

    filterset_fields = [
        'sheet__merchant', 'sheet__customer'
    ]

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method == 'GET':
            return permissions + [IsGuest()]
        return permissions + [CanBuy()]

    @use_transaction(scope='record')
    def create(self, request, *args, **kwargs):  # skipcq
        obj = super().create(request, *args, *kwargs)
        return obj

    def get_queryset(self):
        user = self.request.user
        profile = self.request.profile
        if profile.is_owner:
            where = Q(sheet__merchant=user) | Q(sheet__customer=user)
        elif profile.is_attendant or profile.is_manager:
            where = Q(sheet__merchant=user)
        else:
            where = Q(sheet__customer=user) & Q(profile=profile)
        qs = Record.objects.select_related('sheet', 'attendant', 'profile')
        qs = qs.filter(where)
        qs = qs.order_by('-created')
        return qs


class RecordDetailView(generics.RetrieveDestroyAPIView):

    serializer_class = RecordDetailSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method == 'GET':
            return permissions + [IsGuest()]
        return permissions + [IsManager()]

    def get_queryset(self):
        user = self.request.user
        where = Q(sheet__merchant=user)
        if self.request.method == 'GET':
            where = where | Q(sheet__customer=user)
        qs = Record.objects.select_related(
            'sheet', 'sheet__customer', 'sheet__merchant',
            'attendant', 'profile'
        )
        qs = qs.filter(where)
        return qs

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class SheetRequestView(generics.CreateAPIView):

    serializer_class = SheetRequestSerializer

    permission_classes = [
        IsAuthenticated, IsManager
    ]


class SheetListView(generics.CreateAPIView):

    serializer_class = SheetListSerializer

    permission_classes = [
        IsAuthenticated, IsManager
    ]

    @use_transaction(scope='sheet')
    def create(self, request, *args, **kwargs):  # skipcq
        obj = super().create(request, *args, *kwargs)
        return obj


class SheetDetailView(generics.RetrieveDestroyAPIView):

    serializer_class = SheetDetailSerializer

    permission_classes = [
        IsAuthenticated, IsAttendant
    ]

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method == 'DELETE':
            permissions += [IsManager()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        where = Q(merchant=user)
        if self.request.method == 'GET':
            where = where | Q(customer=user)
        qs = Sheet.objects.select_related('customer', 'merchant')
        qs = qs.filter(where)
        qs = qs.order_by('customer__name')
        return qs

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class SheetBuyerManageView(views.APIView):

    permission_classes = [
        IsAuthenticated, IsManager
    ]

    def get_sheet(self, pk):
        user = self.request.user
        try:
            obj = Sheet.objects.get(pk=pk, customer=user)
            return obj
        except Sheet.DoesNotExist:
            raise NotFound

    def post(self, request, version, pk, profile_id):  # skicq
        data = {'sheet': pk, 'profile': profile_id}
        context = {'request': request}
        serializer = SheetBuyerAddSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.data, status=HTTP_201_CREATED)
        return response

    def delete(self, request, version, pk, profile_id):
        sheet = self.get_sheet(pk)
        sheet.buyers.remove(profile_id)
        response = Response([], status=HTTP_204_NO_CONTENT)
        return response


class BalanceListByMerchantView(generics.ListAPIView):

    serializer_class = BalanceListSerializar

    permission_classes = [
        IsAuthenticated, IsGuest
    ]

    filter_backends = [
        SearchFilter
    ]

    search_fields = [
        'user_name'
    ]

    def get_queryset(self):
        user = self.request.user
        profile = self.request.profile
        qs = Sheet.objects.balance_list_by_merchant(user, profile)
        return qs


class BalanceListByCustomerView(generics.ListAPIView):

    serializer_class = BalanceListSerializar

    permission_classes = [
        IsAuthenticated, IsGuest
    ]

    filter_backends = [
        SearchFilter
    ]

    search_fields = [
        'user_name'
    ]

    def get_queryset(self):
        user = self.request.user
        profile = self.request.profile
        qs = Sheet.objects.balance_list_by_customer(user, profile)
        return qs
