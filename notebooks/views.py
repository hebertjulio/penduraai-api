from django.db.models import Q

from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework import generics, views
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_rw_serializers import generics as rw_generics

from accounts.permissions import IsManager, IsGuest, IsAttendant

from bridges.decorators import load_transaction

from .filters import SheetFilterSet
from .models import Record, Sheet

from .serializers import (
    RecordReadSerializer, RecordWriteSerializer, SheetReadSerializer,
    SheetWriteSerializer, SheetProfileAddSerializer
)


class RecordListView(rw_generics.ListCreateAPIView):

    write_serializer_class = RecordWriteSerializer
    read_serializer_class = RecordReadSerializer

    filterset_fields = [
        'sheet_id'
    ]

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        if self.request.method == 'GET':
            return permissions + [IsGuest()]
        return permissions + [IsAttendant()]

    def get_queryset(self):
        user = self.request.user
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


class RecordConfirmView(views.APIView):

    @classmethod
    def get_sheet(cls, merchant, customer):
        try:
            return Sheet.objects.get(
                merchant=merchant, customer=customer)
        except Sheet.DoesNotExist:
            raise NotFound

    @load_transaction
    def post(self, request, version, transaction_id):
        data = self.transaction.data
        sheet = self.get_sheet(data.pop('merchant'), request.user)
        data = {'sheet': sheet.id, 'signatary': request.user.profile.id}
        record = Record.objects.create(**data)
        serializer = RecordReadSerializer(record)
        self.transaction.status = 'used'
        return Response(serializer.data, HTTP_201_CREATED)


class SheetListView(rw_generics.ListCreateAPIView):

    write_serializer_class = SheetWriteSerializer
    read_serializer_class = SheetReadSerializer
    filterset_class = SheetFilterSet

    def get_queryset(self):
        qs = Sheet.objects.balance_qs()
        return qs


class SheetDetailView(generics.RetrieveDestroyAPIView):

    serializer_class = SheetReadSerializer
    lookup_url_kwarg = 'sheet_id'

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        if self.request.method == 'DELETE':
            return permissions + [IsManager()]
        return permissions + [IsGuest()]

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


class SheetConfirmView(views.APIView):

    permission_classes = [
        IsAuthenticated,
        IsManager
    ]

    @load_transaction
    def post(self, request, version, transaction_id):
        data = self.transaction.data
        data.update({'customer': request.user.id})
        sheet = Sheet.objects.create(**data)
        serializer = SheetReadSerializer(sheet)
        self.transaction.status = 'used'
        return Response(serializer.data, HTTP_201_CREATED)


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
