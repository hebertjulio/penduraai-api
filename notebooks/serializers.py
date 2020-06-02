import json

from django.db.transaction import atomic

from rest_framework import serializers

from accounts.relations import BuyerField, SellerField
from brokers.validators import IsValidTransactionValidator
from brokers.dictdb import Transaction
from brokers.services import send_message

from .models import Record, Customer

from .validators import (
    OweToYourselfValidator, IsCustomerValidator,
    CustomerFromYourselfValidator)


class RecordSerializer(serializers.ModelSerializer):

    transaction = serializers.UUIDField(write_only=True, validators=[
        IsValidTransactionValidator(),
    ])

    debtor = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    seller = SellerField()
    buyer = BuyerField()

    @atomic
    def create(self, validated_data):
        transaction = str(validated_data.pop('transaction'))
        obj = Record(**validated_data)
        obj.save()
        tran = Transaction(transaction)
        tran.status = Transaction.STATUS.accepted
        tran.save()
        send_message(tran.id, json.dumps(tran.data))
        return obj

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = [
            'debtor',
        ]
        validators = [
            OweToYourselfValidator(),
            IsCustomerValidator()
        ]


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

    transaction = serializers.UUIDField(write_only=True, validators=[
        IsValidTransactionValidator(),
    ])

    debtor = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    @atomic
    def create(self, validated_data):
        transaction = str(validated_data.pop('transaction'))
        obj = Customer(**validated_data)
        obj.save()
        tran = Transaction(transaction)
        tran.status = Transaction.STATUS.accepted
        tran.save()
        send_message(tran.id, json.dumps(tran.data))
        return obj

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['authorized']
        validators = [
            CustomerFromYourselfValidator()
        ]
