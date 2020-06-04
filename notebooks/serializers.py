from django.db.transaction import atomic

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from accounts.relations import BuyerField, SellerField
from brokers.validators import IsValidTransactionValidator
from brokers.decorators import accept_transaction

from .models import Record, Customer

from .validators import (
    OweToYourselfValidator, IsCustomerValidator,
    CustomerFromYourselfValidator, PositiveBalanceValidator)


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
    @accept_transaction
    def create(self, validated_data):
        obj = Record(**validated_data)
        obj.save()
        return obj

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = [
            'debtor',
        ]
        validators = [
            OweToYourselfValidator(),
            IsCustomerValidator(),
            PositiveBalanceValidator()
        ]


class CustomerSerializer(serializers.ModelSerializer):

    transaction = serializers.UUIDField(write_only=True, validators=[
        IsValidTransactionValidator(),
    ])

    debtor = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    @atomic
    @accept_transaction
    def create(self, validated_data):
        obj = Customer(**validated_data)
        obj.save()
        return obj

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['authorized']
        validators = [
            CustomerFromYourselfValidator(),
            UniqueTogetherValidator(
                queryset=Customer.objects.all(),
                fields=['creditor', 'debtor']
            )
        ]


class CreditorSerializar(serializers.BaseSerializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        return {
            'id': instance['creditor__id'],
            'name': instance['creditor__name'],
            'balance': instance['balance'] or 0,
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
            'balance': instance['balance'] or 0,
        }

    def to_internal_value(self, data):
        pass
