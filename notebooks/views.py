from django.db.models import Q, Case, When, Value, BooleanField

from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework import generics, views
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_rw_serializers import generics as rw_generics

from accounts.permissions import IsManager, IsGuest, IsAttendant

from bridges.decorators import use_transaction

from .filters import SheetFilterSet
from .models import Record, Sheet

from .serializers import (
    RecordReadSerializer, RecordCreateSerializer, RecordConfirmSerializer,
    SheetReadSerializer, SheetCreateSerializer, SheetConfirmSerializer,
    SheetProfileAddSerializer, SheetUpdateSerializer, SheetByProfileSerializer
)


class RecordListView(rw_generics.ListCreateAPIView):

    write_serializer_class = RecordCreateSerializer
    read_serializer_class = RecordReadSerializer

    filterset_fields = [
        'sheet_id'
    ]

    def initial(self, request, *args, **kwargs):
        request.data.update({'attendant': request.user.profile.id})
        super().initial(request, *args, **kwargs)

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        if self.request.method == 'GET':
            return permissions + [IsGuest()]
        return permissions + [IsAttendant()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Record.objects.none()
        profile = user.profile
        if profile.is_owner:
            where = Q(sheet__merchant=user) | Q(sheet__customer=user)
        elif profile.is_attendant or profile.is_manager:
            where = Q(sheet__merchant=user)
        else:
            where = Q(sheet__customer=user) & Q(signatary=profile)
        qs = Record.objects.select_related('sheet', 'attendant', 'signatary')
        qs = qs.filter(where)
        qs = qs.order_by('-created')
        return qs


class RecordConfirmView(rw_generics.CreateAPIView):

    write_serializer_class = RecordConfirmSerializer
    read_serializer_class = RecordReadSerializer

    @use_transaction(lookup_url_kwarg='transaction_id')
    def create(self, request, *args, **kwargs):
        request.data.update(self.transaction.data)
        return super().create(request, *args, **kwargs)


class RecordDetailView(generics.RetrieveDestroyAPIView):

    serializer_class = RecordReadSerializer
    lookup_url_kwarg = 'record_id'

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        if self.request.method == 'GET':
            return permissions + [IsGuest()]
        return permissions + [IsManager()]

    def get_object(self):
        record_id = self.kwargs[self.lookup_url_kwarg]
        user = self.request.user
        where = Q(sheet__merchant=user)
        if self.request.method == 'GET':
            where = where | Q(sheet__customer=user)
        try:
            obj = Record.objects.get(Q(id=record_id) & (where))
            return obj
        except Record.DoesNotExist:
            raise NotFound

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class SheetListView(rw_generics.ListCreateAPIView):

    write_serializer_class = SheetCreateSerializer
    read_serializer_class = SheetReadSerializer
    filterset_class = SheetFilterSet

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        if self.request.method == 'GET':
            return permissions + [IsGuest()]
        return permissions + [IsManager()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Sheet.objects.none()
        qs = Sheet.objects.balance_qs()
        return qs


class SheetConfirmView(rw_generics.CreateAPIView):

    write_serializer_class = SheetConfirmSerializer
    read_serializer_class = SheetReadSerializer

    permission_classes = [
        IsAuthenticated,
        IsManager
    ]

    @use_transaction(lookup_url_kwarg='transaction_id')
    def create(self, request, *args, **kwargs):
        request.data.update(self.transaction.data)
        return super().create(request, *args, **kwargs)


class SheetDetailView(rw_generics.RetrieveUpdateAPIView):

    write_serializer_class = SheetUpdateSerializer
    read_serializer_class = SheetReadSerializer

    lookup_url_kwarg = 'sheet_id'

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        if self.request.method == 'GET':
            return permissions + [IsGuest()]
        return permissions + [IsManager()]

    def get_object(self):
        sheet_id = self.kwargs[self.lookup_url_kwarg]
        where = Q(merchant=self.request.user)
        if self.request.method == 'GET':
            where = where | Q(customer=self.request.user)
        try:
            return Sheet.objects.get(Q(id=sheet_id) & (where))
        except Sheet.DoesNotExist:
            raise NotFound

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class SheetListByProfileView(generics.ListAPIView):

    serializer_class = SheetByProfileSerializer
    lookup_url_kwarg = 'profile_id'

    permission_classes = [
        IsAuthenticated,
        IsManager
    ]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Sheet.objects.none()
        profile_id = self.kwargs[self.lookup_url_kwarg]
        can_buy = Case(When(
            buyers__id=profile_id, then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
        qs = user.customersheets.filter(is_active=True)
        qs = qs.annotate(can_buy=can_buy)
        return qs


class SheetBuyerView(views.APIView):

    permission_classes = [
        IsAuthenticated,
        IsManager
    ]

    def post(self, request, version, sheet_id, profile_id):  # skipcq
        data = {'sheet': sheet_id, 'profile': profile_id}
        context = {'request': request}
        serializer = SheetProfileAddSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.data, status=HTTP_201_CREATED)
        return response

    def delete(self, request, version, sheet_id, profile_id):  # skipcq
        try:
            sheet = Sheet.objects.get(pk=sheet_id, customer=request.user)
        except Sheet.DoesNotExist:
            raise NotFound
        sheet.buyers.remove(profile_id)
        response = Response([], status=HTTP_204_NO_CONTENT)
        return response
