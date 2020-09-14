from django.db.models import Q

from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework import generics, views
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from accounts.permissions import IsManager
from bridges.decorators import use_ticket

from .serializers import (
    RecordReadSerializer, RecordWriteSerializer, SheetReadSerializer,
    SheetWriteSerializer, SheetProfileAddSerializer
)

from .models import Record, Sheet
from .filters import SheetFilterSet


class RecordConfirmView(views.APIView):

    @classmethod
    def get_sheet(cls, merchant, customer):
        try:
            return Sheet.objects.get(
                merchant=merchant, customer=customer)
        except Sheet.DoesNotExist:
            raise NotFound

    @use_ticket(discard=True, scope='record')
    def post(self, request, version, ticket_id):
        context = {'request': request}
        sheet = self.get_sheet(self.ticket.user, request.user)
        data = {'sheet': sheet.id, 'attendant': self.ticket.profile}
        data.update(self.ticket.data)
        serializer = RecordWriteSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        serializer = RecordReadSerializer(obj)
        return Response(serializer.data, HTTP_201_CREATED)


class RecordListView(generics.ListAPIView):

    serializer_class = RecordReadSerializer

    filterset_fields = [
        'sheet_id'
    ]

    def get_queryset(self):
        user = self.request.user
        profile = self.request.user.profile
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
        permissions = super().get_permissions()
        if self.request.method != 'GET':
            permissions += [IsManager()]
        return permissions

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


class SheetConfirmView(views.APIView):

    def get_permissions(self):
        permissions = super().get_permissions()
        return permissions + [IsManager()]

    @use_ticket(discard=True, scope='sheet')
    def post(self, request, version, ticket_id):
        context = {'request': request}
        data = {'merchant': self.ticket.user}
        serializer = SheetWriteSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        serializer = SheetReadSerializer(obj)
        return Response(serializer.data, HTTP_201_CREATED)


class SheetListView(generics.ListAPIView):

    serializer_class = SheetReadSerializer
    filterset_class = SheetFilterSet

    def get_queryset(self):
        qs = Sheet.objects.balance_qs()
        return qs


class SheetDetailView(generics.RetrieveDestroyAPIView):

    serializer_class = SheetReadSerializer
    lookup_url_kwarg = 'sheet_id'

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method == 'DELETE':
            permissions += [IsManager()]
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


class SheetBuyerView(views.APIView):

    @classmethod
    def get_sheet(cls, user, sheet_id):
        try:
            obj = Sheet.objects.get(pk=sheet_id, customer=user)
            return obj
        except Sheet.DoesNotExist:
            raise NotFound

    def get_permissions(self):
        permissions = super().get_permissions()
        return permissions + [IsManager()]

    def post(self, request, version, sheet_id, profile_id):  # skipcq
        data = {'sheet': sheet_id, 'profile': profile_id}
        context = {'request': request}
        serializer = SheetProfileAddSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.data, status=HTTP_201_CREATED)
        return response

    def delete(self, request, version, sheet_id, profile_id):  # skipcq
        sheet = self.get_sheet(request.user, sheet_id)
        sheet.buyers.remove(profile_id)
        response = Response([], status=HTTP_204_NO_CONTENT)
        return response
