from rest_framework import views
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.response import Response

from accounts.permissions import IsManager, IsAttendant

from .decorators import use_transaction
from .serializers import (
    TransactionSerializer, TransactionProfileSerializer,
    TransactionRecordSerializer, TransactionSheetSerializer
)


class TransactionDetailView(views.APIView):

    @use_transaction
    def get(self, request, version, token, transaction):  # skipcq
        serializer = TransactionSerializer(transaction)
        response = Response(serializer.data, status=HTTP_200_OK)
        return response


class TransactionRejectView(views.APIView):

    @use_transaction(new_status='rejected')
    def put(self, request, version, token, transaction):  # skipcq
        serializer = TransactionSerializer(transaction)
        response = Response(serializer.data, status=HTTP_200_OK)
        return response


class TransactionProfileView(views.APIView):

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [IsManager()]
        return permissions

    def post(self, request, version):  # skipcq
        context = {'request': request}
        serializer = TransactionProfileSerializer(
            data=request.data, context=context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.data, status=HTTP_201_CREATED)
        return response


class TransactionRecordView(views.APIView):

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [IsAttendant()]
        return permissions

    def post(self, request, version):  # skipcq
        context = {'request': request}
        serializer = TransactionRecordSerializer(
            data=request.data, context=context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.data, status=HTTP_201_CREATED)
        return response


class TransactionSheetView(views.APIView):

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [IsManager()]
        return permissions

    def post(self, request, version):  # skipcq
        context = {'request': request}
        serializer = TransactionSheetSerializer(
            data=request.data, context=context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.data, status=HTTP_201_CREATED)
        return response
