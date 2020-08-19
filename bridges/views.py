from rest_framework.status import HTTP_200_OK
from rest_framework import generics, views
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from rest_framework_api_key.permissions import HasAPIKey

from drf_rw_serializers import generics as rw_generics

from accounts.permissions import IsManager, IsAttendant
from accounts.serializers import ProfileScopeSerializer

from notebooks.serializers import SheetScopeSerializer, RecordScopeSerializer

from .serializers import TicketWriteSerializer, TicketReadSerializer
from .models import Ticket
from .services import decode_token, response_ticket
from .exceptions import TokenEncodeException


class TicketListView(rw_generics.CreateAPIView):

    write_serializer_class = TicketWriteSerializer
    read_serializer_class = TicketReadSerializer

    payload_serializers = {
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
        payload_serializer = self.payload_serializers[scope]
        kwargs['payload_serializer'] = payload_serializer()
        return TicketWriteSerializer(*args, **kwargs)


class TicketDetailView(generics.RetrieveAPIView):

    serializer_class = TicketReadSerializer
    lookup_url_kwarg = 'token'

    permission_classes = [
        HasAPIKey
    ]

    def get_object(self):
        try:
            token = self.kwargs[self.lookup_url_kwarg]
            payload = decode_token(token)
            obj = Ticket.objects.get(pk=payload['id'])
            return obj
        except (Ticket.DoesNotExist,
                TokenEncodeException):
            raise NotFound


class TicketDiscardView(views.APIView):

    permission_classes = [
        HasAPIKey
    ]

    def get_object(self, token):
        try:
            payload = decode_token(token)
            obj = Ticket.objects.get(pk=payload['id'])
            return obj
        except (Ticket.DoesNotExist,
                TokenEncodeException):
            raise NotFound

    def put(self, request, version, token):  # skipcq
        obj = self.get_object(token)
        obj.usage = -1
        obj.save()
        serializer = TicketReadSerializer(obj)
        response = Response(serializer.data, status=HTTP_200_OK)
        response_ticket(obj.id, obj.usage)
        return response
