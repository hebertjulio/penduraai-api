from json import dumps

from rest_framework.status import HTTP_200_OK
from rest_framework import generics, views
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from rest_framework_api_key.permissions import HasAPIKey

from drf_rw_serializers import generics as rw_generics

from accounts.permissions import IsManager, IsAttendant
from accounts.serializers import ProfileScopeSerializer

from notebooks.serializers import RecordScopeSerializer, SheetScopeSerializer

from .serializers import TransactionWriteSerializer, TransactionReadSerializer
from .models import Transaction
from .encoders import DecimalEncoder
from .services import decode_token
from .tasks import websocket_send


class TransactionListView(rw_generics.CreateAPIView):

    write_serializer_class = TransactionWriteSerializer
    read_serializer_class = TransactionReadSerializer

    scope_serializers = {
        'profile': ProfileScopeSerializer,
        'sheet': SheetScopeSerializer,
        'record': RecordScopeSerializer
    }

    def get_permissions(self):
        permissions = super().get_permissions()
        scope = self.kwargs['scope']
        if scope == 'record':
            return permissions + [IsAttendant()]
        return permissions + [IsManager()]

    def get_write_serializer(self, *args, **kwargs):
        scope = self.kwargs['scope']
        serializer = self.scope_serializers[scope]()
        kwargs.update({'serializer': serializer})
        return TransactionWriteSerializer(*args, **kwargs)


class TransactionDetailView(generics.RetrieveAPIView):

    lookup_url_kwarg = 'token'

    permission_classes = [
        HasAPIKey
    ]

    def get_object(self):
        try:
            token = self.kwargs[self.lookup_url_kwarg]
            payload = decode_token(token)
            obj = Transaction.objects.get(pk=payload['id'])
            return obj
        except Transaction.DoesNotExist:
            raise NotFound

    def get_serializer(self,  *args, **kwargs):
        kwargs.update({'exclude': ['token']})
        serializer = TransactionReadSerializer(*args, **kwargs)
        return serializer


class TransactionDiscardView(views.APIView):

    permission_classes = [
        HasAPIKey
    ]

    def get_object(self, token):
        try:
            payload = decode_token(token)
            obj = Transaction.objects.get(pk=payload['id'])
            return obj
        except Transaction.DoesNotExist:
            raise NotFound

    def put(self, request, version, token):  # skipcq
        obj = self.get_object(token)
        obj.usage = -1
        obj.save()
        serializer = TransactionReadSerializer(obj)
        response = Response(serializer.data, status=HTTP_200_OK)
        group = str(obj.id)
        message = dumps(serializer.data, cls=DecimalEncoder)
        websocket_send.apply_async((group, message))
        return response
