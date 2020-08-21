from rest_framework.status import HTTP_200_OK
from rest_framework import views
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from accounts.permissions import IsManager, IsAttendant

from .serializers import TicketSerializer
from .db import Ticket
from .services import get_token_data, send_ws_message
from .tasks import push_notification


class TicketListView(views.APIView):

    def get_permissions(self):
        permissions = super().get_permissions()
        scope = self.kwargs['scope']
        if scope == 'record':
            return permissions + [IsAttendant()]
        return permissions + [IsManager()]

    def post(self, request, version, scope):  # skipcq
        request.data.update({'scope': scope})
        serializer = TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.data, status=HTTP_200_OK)
        return response


class TicketDetailView(views.APIView):

    permission_classes = [
        HasAPIKey
    ]

    def get(self, request, version, token):  # skipcq
        data = get_token_data(token)
        ticket = Ticket(data['scope'], data['key'])
        ticket.exist(raise_exception=True)
        serializer = TicketSerializer(ticket)
        response = Response(serializer.data, status=HTTP_200_OK)
        return response


class TicketDiscardView(views.APIView):

    permission_classes = [
        HasAPIKey
    ]

    def put(self, request, version, token):  # skipcq
        data = get_token_data(token)
        ticket = Ticket(data['scope'], data['key'])
        ticket.exist(raise_exception=True)
        send_ws_message(ticket.key, 'rejected')
        push_notification.apply([ticket.key, '*message*'])
        serializer = TicketSerializer(ticket)
        response = Response(serializer.data, status=HTTP_200_OK)
        ticket.discard()
        return response
