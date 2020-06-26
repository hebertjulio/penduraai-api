from django.db.models import Q

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from accounts.permissions import IsManager, IsAttendant, IsGuest

from bridges.decorators import use_transaction

from .permissions import CanBuy
from .models import Record, Sheet, Buyer
from .serializers import (
    RecordReadSerializer, RecordCreateSerializer, RecordRequestSerializer,
    SheetReadSerializer, SheetCreateSerializer, SheetRequestSerializer,
    BalanceSerializar, BuyerSerializer
)


class RecordRequestView(generics.CreateAPIView):

    serializer_class = RecordRequestSerializer
    permission_classes = [
        IsAuthenticated, IsAttendant
    ]


class RecordTransactionView(generics.CreateAPIView):

    serializer_class = RecordCreateSerializer
    permission_classes = [
        IsAuthenticated, CanBuy
    ]

    @use_transaction(scope='record')
    def create(self, request, *args, **kwargs):  # skipcq
        request.data.update(self.transaction.get_data())
        obj = super().create(request, *args, *kwargs)
        return obj


class RecordListView(generics.ListAPIView):

    serializer_class = RecordReadSerializer
    permission_classes = [
        IsAuthenticated, IsGuest
    ]
    filterset_fields = [
        'sheet__store', 'sheet__customer'
    ]

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
    serializer_class = RecordReadSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method == 'GET':
            return permissions + [IsGuest()]
        return permissions + [IsManager()]

    def get_queryset(self):
        user = self.request.user
        where = Q(sheet__store=user)
        if self.request.method == 'GET':
            where = where | Q(sheet__customer=user)
        qs = Record.objects.select_related(
            'sheet', 'sheet__customer', 'sheet__store',
            'attendant', 'signature'
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


class SheetTransactionView(generics.CreateAPIView):

    serializer_class = SheetCreateSerializer

    permission_classes = [
        IsAuthenticated, IsManager
    ]

    @use_transaction(scope='sheet')
    def create(self, request, *args, **kwargs):  # skipcq
        request.data.update(self.transaction.get_data())
        obj = super().create(request, *args, *kwargs)
        return obj


class SheetDetailView(generics.RetrieveDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = SheetReadSerializer

    permission_classes = [
        IsAuthenticated, IsAttendant
    ]

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method == 'DELETE':
            permissions = +[IsManager()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        where = Q(store=user)
        if self.request.method == 'GET':
            where = where | Q(customer=user)
        qs = Sheet.objects.select_related('customer', 'store')
        qs = qs.filter(where)
        qs = qs.order_by('customer__name')
        return qs

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class BuyerListView(generics.ListCreateAPIView):

    serializer_class = BuyerSerializer
    permission_classes = [
        IsAuthenticated, IsManager
    ]

    def get_queryset(self):
        user = self.request.user
        qs = Buyer.objects.select_related('sheet', 'profile')
        qs = qs.filter(profile__user=user)
        qs = qs.order_by('profile__name')
        return qs


class BuyerDetailView(generics.DestroyAPIView):

    serializer_class = BuyerSerializer
    permission_classes = [
        IsAuthenticated, IsManager
    ]

    def get_queryset(self):
        user = self.request.user
        qs = Buyer.objects.filter(profile__user=user)
        return qs


class BalanceListByStoreView(generics.ListAPIView):

    serializer_class = BalanceSerializar
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
        profile = user.profile
        qs = Sheet.objects.balance_list_by_store(user, profile)
        return qs


class BalanceListByCustomerView(generics.ListAPIView):

    serializer_class = BalanceSerializar
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
        profile = user.profile
        qs = Sheet.objects.balance_list_by_customer(user, profile)
        return qs
