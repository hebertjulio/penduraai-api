import datetime

from django.utils import timezone

from rest_framework.status import HTTP_200_OK
from rest_framework import generics, views
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from drf_rw_serializers import generics as rw_generics

from rest_framework_api_key.permissions import HasAPIKey

from accounts.permissions import (
    IsAuthenticatedAndProfileIsManager, IsAuthenticatedAndProfileIsAttendant)

from .serializers import TransactionWriteSerializer, TransactionReadSerializer
from .models import Transaction


class TransactionListView(rw_generics.CreateAPIView):

    write_serializer_class = TransactionWriteSerializer
    read_serializer_class = TransactionReadSerializer

    def get_permissions(self):
        scope = self.kwargs['scope']
        if scope == 'record':
            return [IsAuthenticatedAndProfileIsAttendant()]
        return [IsAuthenticatedAndProfileIsManager()]

    def perform_create(self, serializer):
        expire_at = timezone.now() + datetime.timedelta(minutes=30)
        serializer.save(scope=self.kwargs['scope'], expire_at=expire_at)


class TransactionDetailView(generics.RetrieveAPIView):

    serializer_class = TransactionReadSerializer
    queryset = Transaction.objects.all()
    lookup_url_kwarg = 'transaction_id'

    permission_classes = [
        HasAPIKey
    ]


class TransactionDiscardView(views.APIView):

    @classmethod
    def get_object(cls, pk):
        try:
            obj = Transaction.objects.get(id=pk)
            return obj
        except Transaction.DoesNotExist:
            raise NotFound

    def put(self, request, version, transaction_id):  # skipcq
        obj = self.get_object(transaction_id)
        obj.discarded = True
        obj.save()
        serializer = TransactionReadSerializer(obj)
        response = Response(serializer.data, status=HTTP_200_OK)
        return response
