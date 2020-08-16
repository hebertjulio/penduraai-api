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
from .permissions import HasTransaction


class TransactionListView(rw_generics.CreateAPIView):

    write_serializer_class = TransactionWriteSerializer
    read_serializer_class = TransactionReadSerializer

    scopes_serializers = {
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
        serializer = self.scopes_serializers[scope]()
        kwargs.update({'serializer': serializer})
        return TransactionWriteSerializer(*args, **kwargs)


class TransactionDetailView(generics.RetrieveAPIView):

    queryset = Transaction.objects.all()
    lookup_url_kwarg = 'transaction_id'

    permission_classes = [
        HasAPIKey, HasTransaction
    ]

    def get_object(self):
        pk = self.kwargs[self.lookup_url_kwarg]
        obj = self.request.transaction
        if obj.id != pk:
            raise NotFound
        return obj

    def get_serializer(self,  *args, **kwargs):
        kwargs.update({'exclude': ['token']})
        serializer = TransactionReadSerializer(*args, **kwargs)
        return serializer


class TransactionDiscardView(views.APIView):

    permission_classes = [
        HasAPIKey, HasTransaction
    ]

    def get_object(self, pk):
        obj = self.request.transaction
        if obj.id != pk:
            raise NotFound
        return obj

    def put(self, request, version, transaction_id):  # skipcq
        obj = self.get_object(transaction_id)
        obj.usage = -1
        obj.save()
        serializer = TransactionReadSerializer(obj)
        response = Response(serializer.data, status=HTTP_200_OK)
        return response
