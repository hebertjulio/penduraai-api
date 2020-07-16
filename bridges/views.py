import json

from rest_framework.status import HTTP_200_OK
from rest_framework import generics, views
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .serializers import TransactionDetailSerializer
from .models import Transaction
from .services import send_message
from .encoders import DecimalEncoder


class TransactionDetailView(generics.RetrieveAPIView):

    serializer_class = TransactionDetailSerializer
    queryset = Transaction.objects.all()
    lookup_url_kwarg = 'transaction_id'


class TransactionDiscardView(views.APIView):

    serializer_class = TransactionDetailSerializer

    def put(self, request, version, transaction_id):
        try:
            obj = Transaction.objects.get(
                id=transaction_id, status=Transaction.STATUS.not_used)
        except Transaction.DoesNotExist:
            raise NotFound

        obj = self.get_object(transaction_id)
        obj.status = Transaction.STATUS.discarded
        obj.save()

        serializer = TransactionDetailSerializer(obj)
        response = Response(serializer.data, status=HTTP_200_OK)
        message = json.dumps(serializer.data, cls=DecimalEncoder)
        send_message(obj.id, message)
        return response
