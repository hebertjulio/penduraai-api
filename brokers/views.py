import json

from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView

from rest_framework_api_key.permissions import HasAPIKey

from .dictdb import Transaction
from .serializers import TransactionSerializer
from .services import push_notification


class TransactionListView(APIView):

    permission_classes = [HasAPIKey]

    def post(self, request):  # skipcq
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TransactionDetailView(APIView):

    permission_classes = [HasAPIKey]

    def get(self, request, pk):  # skipcq
        tran = Transaction(pk)
        if not tran.exist():
            raise NotFound
        return Response(tran.data, status=HTTP_200_OK)


class TransactionRejectView(APIView):

    permission_classes = [HasAPIKey]

    def put(self, request, pk):  # skipcq
        tran = Transaction(pk)
        if not tran.exist():
            raise NotFound
        tran.status = Transaction.STATUS.rejected
        push_notification(tran.id, json.dumps(tran.data))
        return Response(tran.data, status=HTTP_200_OK)
