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
        extra_kwargs = {
            'customer_record': {
                'validators': [
                    IsCustomerRecordOwnerValidator()
                ]
            }
        }
        validators = [
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


class CreditorSerializar(serializers.BaseSerializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        return {
            'id': instance['creditor__id'],
            'name': instance['creditor__name'],
            'balance': instance['balance'] or 0.0,
        }

    def to_internal_value(self, data):
        pass


class DebtorSerializar(serializers.BaseSerializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        return {
            'id': instance['debtor__id'],
            'name': instance['debtor__name'],
            'balance': instance['balance'] or 0.0,
        }

    def to_internal_value(self, data):
        pass
