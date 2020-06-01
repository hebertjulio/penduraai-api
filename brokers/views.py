import json

from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView

from .dictdb import Transaction
from .serializers import TransactionSerializer
from .services import send_message


class TransactionListView(APIView):

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TransactionDetailView(APIView):

    def get(self, request, pk, format=None):
        tran = Transaction(pk)
        if not tran.exist():
            raise NotFound
        data = {'id': tran.id, 'payload': tran.payload, 'status': tran.status}
        return Response(data, status=HTTP_200_OK)


class TransactionRejectView(APIView):

    def put(self, request, pk, format=None):
        tran = Transaction(pk)
        if not tran.exist():
            raise NotFound
        tran.status = Transaction.STATUS.rejected
        data = {'id': tran.id, 'payload': tran.payload, 'status': tran.status}
        send_message(tran.id, json.dumps(tran.data))
        return Response(data, status=HTTP_200_OK)
