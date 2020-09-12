from rest_framework.status import HTTP_200_OK
from rest_framework import views
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from accounts.permissions import IsManager, IsAttendant

from .serializers import TicketWriteSerializer, TicketReadSerializer
from .decorators import use_ticket


class TicketListView(views.APIView):

    def get_permissions(self):
        permissions = super().get_permissions()
        scope = self.kwargs['scope']
        if scope == 'record':
            return permissions + [IsAttendant()]
        return permissions + [IsManager()]

    def post(self, request, version, scope):  # skipcq
        request.data.update({'scope': scope, 'expire': 1800})
        context = {'request': request}
        serializer = TicketWriteSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save()
        serializer = TicketReadSerializer(ticket)
        return Response(serializer.data, status=HTTP_200_OK)


class TicketDetailView(views.APIView):

    permission_classes = [
        HasAPIKey
    ]

    @use_ticket(discard=False)
    def get(self, request, version, token):  # skipcq
        serializer = TicketReadSerializer(self.ticket, exclude=['token'])
        return Response(serializer.data, status=HTTP_200_OK)


class TicketDiscardView(views.APIView):

    permission_classes = [
        HasAPIKey
    ]

    @use_ticket(discard=True)
    def put(self, request, version, token):  # skipcq
        serializer = TicketReadSerializer(self.ticket, exclude=['token'])
        return Response(serializer.data, status=HTTP_200_OK)
