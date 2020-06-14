import uuid

from django.db.transaction import atomic

from rest_framework import serializers

from accounts.relations import UserRelatedField, ProfileRelatedField

from .decorators import accept_transaction
from .models import Record, Sheet
from .dictdb import Transaction

from .validators import (
    IsSheetOwnerValidator, CustomerFromYourselfValidator,
    AlreadyACustomerValidator, SellerAccountableValidator,
    BuyerAccountableValidator, TransactionExistValidator,
    TransactionSignatureValidator, TransactionStatusValidator
)

from .relations import SheetRelatedField


class RecordSerializer(serializers.ModelSerializer):

    transaction = serializers.UUIDField(validators=[
        TransactionExistValidator(),
        TransactionSignatureValidator(),
        TransactionStatusValidator()
    ], write_only=True)

    sheet = SheetRelatedField()
    buyer = ProfileRelatedField(read_only=True)
    seller = ProfileRelatedField()

    @atomic
    @accept_transaction
    def create(self, validated_data):
        request = self.context['request']
        obj = Record(**validated_data)
        obj.buyer = request.user.profile
        obj.save()
        return obj

    class Meta:
        model = Record
        fields = '__all__'
        extra_kwargs = {
            'sheet': {
                'validators': [
                    IsSheetOwnerValidator()
                ]
            }
        }
        validators = [
            SellerAccountableValidator(),
            BuyerAccountableValidator()
        ]


class SheetSerializer(serializers.ModelSerializer):

    transaction = serializers.UUIDField(validators=[
        TransactionExistValidator(),
        TransactionSignatureValidator(),
        TransactionStatusValidator()
    ], write_only=True)

    store = UserRelatedField()
    customer = UserRelatedField(read_only=True)

    @atomic
    @accept_transaction
    def create(self, validated_data):
        request = self.context['request']
        obj = Sheet(**validated_data)
        obj.customer = request.user
        obj.save()
        return obj

    class Meta:
        model = Sheet
        fields = '__all__'
        read_only_fields = ['authorized']
        validators = [
            CustomerFromYourselfValidator(),
            AlreadyACustomerValidator()
        ]


class BalanceSerializar(serializers.BaseSerializer):

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    def to_representation(self, instance):
        return {
            'sheet_id': instance['sheet_id'],
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
    store = serializers.IntegerField(read_only=True)

    status = serializers.ChoiceField(
        choices=Transaction.STATUS, read_only=True
    )

    ttl = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        request = self.context['request']
        if validated_data['action'] == Transaction.ACTION.new_record:
            validated_data['payload'].update({
                'seller': request.user.profile.id
            })
        tran = Transaction(str(uuid.uuid4()))
        tran.action = validated_data['action']
        tran.store = request.user.id
        tran.payload = validated_data['payload']
        tran.save(60*30)  # 30 minutes
        return tran.data

    def update(self, instance, validated_data):
        raise NotImplementedError
