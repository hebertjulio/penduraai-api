import uuid
import json

from django.db import transaction

from rest_framework import serializers

from accounts.relations import BuyerField, SellerField, CreditorField

from .models import Record, Customer
from .services import transaction_response
from .dictdb import Storage

from .validators import (
    CreditorAndDebtorSameUserValidator, TransactionIdValidator
)


class RecordSerializer(serializers.ModelSerializer):

    buyer = BuyerField()

    @transaction.atomic
    def create(self, validated_data):
        obj = Record(**validated_data)
        obj.save()
        transaction_response(str(obj.id), 'ACCEPTED')
        return obj

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = [
            'debtor', 'creditor', 'seller', 'operation',
            'description', 'value',
        ]
        validators = [
            TransactionIdValidator(),
            CreditorAndDebtorSameUserValidator(),
        ]


class RecordTransactionSerializer(serializers.Serializer):

    description = serializers.CharField(max_length=255)
    operation = serializers.ChoiceField(choices=Record.OPERATION)

    creditor = CreditorField()
    seller = SellerField()

    value = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Record.MIN_VALUE
    )

    channel_name = serializers.CharField()

    def create(self, validated_data):
        data = self.data.copy()
        data.update({'id': str(uuid.uuid4())})
        db = Storage(data['id'])
        channel_name = Storage.Item(data.pop('channel_name'), 86460)
        record = Storage.Item(json.dumps(data), 86400)
        db['channel_name'] = channel_name
        db['record'] = record
        return data

    def update(self, instance, validated_data):
        pass


class CreditorSerializar(serializers.BaseSerializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        balance = instance['payment_sum'] - instance['debt_sum']
        return {
            'id': instance['creditor__id'],
            'name': instance['creditor__name'],
            'balance': balance,
        }

    def to_internal_value(self, data):
        pass


class DebtorSerializar(serializers.BaseSerializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        balance = instance['payment_sum'] - instance['debt_sum']
        return {
            'id': instance['debtor__id'],
            'name': instance['debtor__name'],
            'balance': balance,
        }

    def to_internal_value(self, data):
        pass


class CustomerSerializer(serializers.ModelSerializer):

    creditor = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Customer
        fields = '__all__'
