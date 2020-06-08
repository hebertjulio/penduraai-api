import uuid

from django.db.transaction import atomic

from rest_framework import serializers

from .decorators import accept_transaction
from .models import Record, CustomerRecord
from .dictdb import Transaction
from .validators import (
    IsCustomerRecordOwnerValidator, CustomerFromYourselfValidator,
    AlreadyACustomerValidator, SellerAccountableValidator,
    BuyerAccountableValidator, TransactionExistValidator,
    TransactionSignatureValidator, TransactionStatusValidator
)


class RecordSerializer(serializers.ModelSerializer):

    transaction = serializers.UUIDField(write_only=True, validators=[
        TransactionExistValidator(),
        TransactionSignatureValidator(),
        TransactionStatusValidator()
    ])

    @atomic
    @accept_transaction
    def create(self, validated_data):
        request = self.context['request']
        obj = Record(**validated_data)
        obj.buyer = request.profile
        obj.save()
        return obj

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = [
            'buyer'
        ]
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
        TransactionExistValidator(),
        TransactionSignatureValidator(),
        TransactionStatusValidator()
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


class TransactionSerializer(serializers.Serializer):

    id = serializers.UUIDField(read_only=True)
    action = serializers.ChoiceField(choices=Transaction.ACTION)
    payload = serializers.JSONField(binary=True)
    creditor = serializers.IntegerField(read_only=True)

    status = serializers.ChoiceField(
        choices=Transaction.STATUS, read_only=True
    )

    ttl = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        request = self.context['request']
        if validated_data['action'] == Transaction.ACTION.new_record:
            validated_data['payload'].update({
                'seller': request.profile.id
            })
        tran = Transaction(str(uuid.uuid4()))
        tran.action = validated_data['action']
        tran.creditor = request.user.id
        tran.payload = validated_data['payload']
        tran.save(60*30)  # 30 minutes
        return tran.data

    def update(self, instance, validated_data):
        raise NotImplementedError
