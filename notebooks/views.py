from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from .models import Record, Customer

from .serializers import (
    RecordSerializer, CreditorSerializar, DebtorSerializar,
    CustomerSerializer
)


class RecordListView(generics.ListCreateAPIView):

    serializer_class = RecordSerializer
    filterset_fields = (
        'creditor', 'debtor',
    )

    def get_queryset(self):
        user = self.request.user
        qs = Record.objects.filter(Q(creditor=user) | Q(debtor=user))
        return qs


class RecordDetailView(generics.RetrieveAPIView):

    lookup_field = 'pk'
    serializer_class = RecordSerializer
    queryset = Record.objects.all()


class CreditorListView(APIView):

    def get(_, request):
        user = request.user
        rows = Customer.objects.creditors(user.id)
        serializer = CreditorSerializar(rows, many=True)
        return Response(serializer.data, HTTP_200_OK)


class DebtorListView(generics.ListAPIView):

    def get(_, request):
        user = request.user
        rows = Customer.objects.debtors(user.id)
        serializer = DebtorSerializar(rows, many=True)
        return Response(serializer.data, HTTP_200_OK)


class CustomerListView(generics.ListCreateAPIView):

    serializer_class = CustomerSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Customer.objects.filter(creditor=user)
        return qs


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = CustomerSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Customer.objects.filter(creditor=user)
        return qs
