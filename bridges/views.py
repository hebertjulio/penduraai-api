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


class TransactionDiscardView(views.APIView):

    serializer_class = TransactionDetailSerializer
    queryset = Transaction.objects.all()

    @classmethod
    def get_object(cls, pk):
        try:
            tran = Transaction.objects.get(pk=pk)
            return tran
        except Transaction.DoesNotExist:
            raise NotFound

    def put(self, request, version, pk):  # skipcq
        obj = self.get_object(pk)
        obj.status = Transaction.STATUS.discarded
        obj.save()
        serializer = TransactionDetailSerializer(obj)
        response = Response(serializer.data, status=HTTP_200_OK)
        message = json.dumps(serializer.data, cls=DecimalEncoder)
        send_message(obj.id, message)
        return response
