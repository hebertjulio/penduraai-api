from django.db.transaction import atomic

from rest_framework import serializers

from accounts.relations import BuyerField, SellerField

from .models import Record, Customer
from .services import transaction_response

from .validators import (
    CreditorAndDebtorSameUserValidator, TransactionExistValidator
)


class RecordSerializer(serializers.ModelSerializer):

    transaction = serializers.CharField(max_length=255, write_only=True)
    buyer = BuyerField()

    @atomic
    def create(self, validated_data):
        transaction = validated_data.pop('transaction')
        obj = Record(**validated_data)
        obj.save()
        transaction_response(transaction, 'ACCEPTED')
        return obj

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = [
            'debtor', 'creditor', 'seller', 'operation',
            'description', 'value',
        ]
        validators = [
            TransactionExistValidator(),
            CreditorAndDebtorSameUserValidator(),
        ]


class RecordTransactionSerializer(serializers.ModelSerializer):

    seller = SellerField()

    def create(self, validated_data):
        return validated_data

    class Meta:
        model = Record
        exclude = [
            'debtor', 'buyer'
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

    creditor = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Customer
        fields = '__all__'
