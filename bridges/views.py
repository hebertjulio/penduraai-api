from rest_framework.status import HTTP_200_OK
from rest_framework import views
from rest_framework.response import Response

from rest_framework_api_key.permissions import HasAPIKey

from .serializers import TransactionReadSerializer
from .decorators import load_transaction


class TransactionDetailView(views.APIView):

    permission_classes = [
        HasAPIKey
    ]

    @load_transaction
    def get(self, request, version, transaction_id):  # skipcq
        serializer = TransactionReadSerializer(self.transaction)
        return Response(serializer.data, status=HTTP_200_OK)


class TransactionDiscardView(views.APIView):

    permission_classes = [
        HasAPIKey
    ]

    @load_transaction
    def put(self, request, version, transaction_id):  # skipcq
        self.transaction.status = 'discarded'
        serializer = TransactionReadSerializer(self.transaction)
        return Response(serializer.data, status=HTTP_200_OK)
