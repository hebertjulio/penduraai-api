from rest_framework.status import HTTP_200_OK
from rest_framework import views
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from accounts.permissions import IsManager, IsAttendant

from .serializers import TicketSerializer
from .db import Ticket
from .services import token_decode, send_ws_message


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
        data = token_decode(token)
        ticket = Ticket(data['id'])
        ticket.exist(raise_exception=True)
        serializer = TicketSerializer(ticket, exclude=['token'])
        response = Response(serializer.data, status=HTTP_200_OK)
        return response


class TicketDiscardView(views.APIView):

    permission_classes = [
        HasAPIKey
    ]

    def put(self, request, version, token):  # skipcq
        data = token_decode(token)
        ticket = Ticket(data['id'])
        ticket.exist(raise_exception=True)
        ticket.status = 'discarded'
        send_ws_message(ticket.id, ticket.status)
        serializer = TicketSerializer(ticket, exclude=['token'])
        response = Response(serializer.data, status=HTTP_200_OK)
        return response
