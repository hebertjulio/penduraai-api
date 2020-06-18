from django.db.models import Q

from rest_framework.status import HTTP_201_CREATED
from rest_framework import generics, views
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from accounts.permissions import IsManager, IsAttendant

from bridges.decorators import use_transaction

from .permissions import CanBuy
from .models import Record, Sheet, Buyer
from .serializers import (
    RecordSerializer, SheetSerializer, BalanceSerializar, BuyerSerializer
)


class RecordCreateView(views.APIView):

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [CanBuy()]
        return permissions

    @use_transaction(
        scope='record', current_status='awaiting', new_status='accepted')
    def post(self, request, version, token, transaction=None):  # skipcq
        payload = transaction.payload
        context = {'request': request}
        serializer = RecordSerializer(data=payload, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.data, status=HTTP_201_CREATED)
        return response


class RecordListView(generics.ListAPIView):

    serializer_class = RecordSerializer
    filterset_fields = [
        'sheet__store',
        'sheet__customer',
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
        instance.is_active = False
        instance.save()


class SheetCreateView(views.APIView):

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [IsManager()]
        return permissions

    @use_transaction(
        scope='sheet', current_status='awaiting', new_status='accepted')
    def post(self, request, version, token, transaction=None):  # skipcq
        payload = transaction.payload
        context = {'request': request}
        serializer = SheetSerializer(data=payload, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.data, status=HTTP_201_CREATED)
        return response


class SheetDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = SheetSerializer

    def get_permissions(self):
        permission_classes = super().permission_classes
        permission_classes = [
            permission_classes[0] & (IsAttendant)
        ]
        if self.request.method in ['DELETE', 'PATCH', 'PUT']:
            permission_classes = [
                permission_classes[0] & IsManager
            ]
        self.permission_classes = permission_classes
        permissions = super().get_permissions()
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
