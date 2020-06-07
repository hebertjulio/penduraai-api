import json

from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from .dictdb import Transaction
from .serializers import TransactionSerializer
from .services import send_message


class TransactionListView(APIView):

    def post(self, request):  # skipcq
        context = {'request': request}
        serializer = TransactionSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class TransactionDetailView(APIView):

    def get(self, request, pk):  # skipcq
        tran = Transaction(pk)
        if not tran.exist():
            raise NotFound
        return Response(tran.data, status=HTTP_200_OK)


class TransactionRejectView(APIView):

    def put(self, request, pk):  # skipcq
        tran = Transaction(pk)
        if not tran.exist():
            raise NotFound
        tran.status = Transaction.STATUS.rejected
        tran.save()
        send_message(tran.id, json.dumps(tran.data))
        return Response(tran.data, status=HTTP_200_OK)
