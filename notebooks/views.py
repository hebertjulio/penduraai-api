from django.db.models import Q

from rest_framework import generics, views
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from accounts.permissions import (
    IsAuthenticatedAndProfileIsManager, IsAuthenticatedAndProfileIsAttendant
)

from bridges.decorators import use_transaction

from .models import Record, Sheet

from .serializers import (
    RecordRequestSerializer, RecordCreateSerializer, RecordListSerializer,
    RecordDetailSerializer, SheetRequestSerializer, SheetCreateSerializer,
    SheetListSerializer, SheetDetailSerializer, SheetProfileAddSerializer
)


class RecordRequestView(generics.CreateAPIView):

    serializer_class = RecordRequestSerializer
    permission_classes = [
        IsAuthenticatedAndProfileIsAttendant
    ]


class RecordCreateView(generics.CreateAPIView):

    serializer_class = RecordCreateSerializer

    @use_transaction(scope='record', lookup_url_kwarg='transaction_id')
    def create(self, request, *args, **kwargs):
        request.data.update(self.transaction.get_data())
        obj = super().create(request, *args, *kwargs)
        return obj


class RecordListView(generics.ListAPIView):

    serializer_class = RecordListSerializer
    filterset_fields = [
        'sheet__merchant', 'sheet__customer'
    ]

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
    lookup_url_kwarg = 'record_id'

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method == 'GET':
            return permissions
        return [IsAuthenticatedAndProfileIsManager()]

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


class SheetRequestView(generics.CreateAPIView):

    serializer_class = SheetRequestSerializer
    permission_classes = [
        IsAuthenticatedAndProfileIsManager
    ]


class SheetCreateView(generics.CreateAPIView):

    serializer_class = SheetCreateSerializer
    permission_classes = [
        IsAuthenticatedAndProfileIsManager
    ]

    @use_transaction(scope='sheet', lookup_url_kwarg='transaction_id')
    def create(self, request, *args, **kwargs):
        request.data.update(self.transaction.get_data())
        obj = super().create(request, *args, *kwargs)
        return obj


class SheetDetailView(generics.RetrieveDestroyAPIView):

    serializer_class = SheetDetailSerializer
    lookup_url_kwarg = 'sheet_id'

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method == 'DELETE':
            return [IsAuthenticatedAndProfileIsManager()]
        return permissions

    def get_object(self):
        sheet_id = self.kwargs[self.lookup_url_kwarg]
        user = self.request.user
        where = Q(merchant=user)
        if self.request.method == 'GET':
            where = where | Q(customer=user)
        try:
            obj = Sheet.objects.get(Q(id=sheet_id) & (where))
            return obj
        except Sheet.DoesNotExist:
            raise NotFound

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class SheetProfileManageView(views.APIView):

    permission_classes = [
        IsAuthenticatedAndProfileIsManager
    ]

    def get_sheet(self, sheet_id):
        user = self.request.user
        try:
            obj = Sheet.objects.get(pk=sheet_id, customer=user)
            return obj
        except Sheet.DoesNotExist:
            raise NotFound

    def post(self, request, version, sheet_id, profile_id):
        data = {'sheet': sheet_id, 'profile': profile_id}
        context = {'request': request}
        serializer = SheetProfileAddSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.data, status=HTTP_201_CREATED)
        return response

    def delete(self, request, version, sheet_id, profile_id):
        sheet = self.get_sheet(sheet_id)
        sheet.profiles.remove(profile_id)
        response = Response([], status=HTTP_204_NO_CONTENT)
        return response


class SheetListView(generics.ListAPIView):

    serializer_class = SheetListSerializer
    filter_backends = [
        SearchFilter
    ]
    search_fields = [
        'merchant__name',
        'customer__name',
    ]

    def get_queryset(self):
        qs = Sheet.objects.balances()
        by = self.kwargs['by']
        if by == 'merchant':
            qs = qs.filter(customer=self.request.user)
        else:
            qs = qs.filter(merchant=self.request.user)
        profile = self.request.profile
        if not profile.is_owner:
            qs = qs.filter(profiles=profile)
        qs = qs.order_by(by + '__name')
        return qs
