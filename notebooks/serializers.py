from django.db.transaction import atomic

from rest_framework import serializers

from brokers.validators import IsValidTransactionValidator
from brokers.decorators import accept_transaction

from .models import Record, CustomerRecord

from .validators import (
    IsCustomerRecordOwnerValidator, CustomerFromYourselfValidator,
    AlreadyACustomerValidator, SellerAccountableValidator,
    BuyerAccountableValidator)


class RecordSerializer(serializers.ModelSerializer):

    transaction = serializers.UUIDField(write_only=True, validators=[
        IsValidTransactionValidator(),
    ])

    @atomic
    @accept_transaction
    def create(self, validated_data):
        obj = Record(**validated_data)
        obj.save()
        return obj

    class Meta:
        model = Record
        fields = '__all__'
        validators = [
            IsCustomerRecordOwnerValidator(),
            SellerAccountableValidator(),
            BuyerAccountableValidator()
        ]


class CustomerRecordSerializer(serializers.ModelSerializer):

    transaction = serializers.UUIDField(write_only=True, validators=[
        IsValidTransactionValidator(),
    ])

    @atomic
    @accept_transaction
    def create(self, validated_data):
        request = self.context['request']
        obj = CustomerRecord(**validated_data)
        obj.debtor = request.user
        obj.save()
        return obj

    class Meta:
        model = CustomerRecord
        fields = '__all__'
        read_only_fields = ['authorized', 'debtor']
        validators = [
            CustomerFromYourselfValidator(),
            AlreadyACustomerValidator()
        ]
        extra_kwargs = {
            'creditor': {
                'write_only': True
            }
        }


class CreditorDebtorSerializar(serializers.BaseSerializer):

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    def to_representation(self, instance):
        return {
            'user_id': instance['user_id'],
            'user_name': instance['user_name'],
            'balance': instance['balance'],
        }

    def to_internal_value(self, data):
        raise NotImplementedError
