from django.db.transaction import atomic
from rest_framework import serializers

from accounts.relations import BuyerField, SellerField
from brokers.validators import (
    TransactionValidator, TransactionSignatureValidator)

from brokers.dictdb import Transaction

from .models import Record, Customer

from .validators import (
    CreditorAndDebtorSameUserValidator)


class RecordSerializer(serializers.ModelSerializer):

    transaction = serializers.UUIDField(write_only=True, validators=[
        TransactionValidator(),
        TransactionSignatureValidator([
            'creditor', 'seller', 'operation', 'value',
            'description',
        ]),
    ])

    buyer = BuyerField()
    seller = SellerField()

    @atomic
    def create(self, validated_data):
        tid = str(validated_data.pop('transaction'))
        request = self.context['request']
        obj = Record(**validated_data)
        obj.debtor = request.user
        obj.save()
        tran = Transaction(tid)
        tran.status = Transaction.STATUS.accepted
        return obj

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = [
            'debtor',
        ]
        validators = [
            CreditorAndDebtorSameUserValidator()
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
