import uuid

from django.db.transaction import atomic

from rest_framework import serializers

from accounts.relations import UserRelatedField, ProfileRelatedField
from accounts.validators import ProfileBelongUserValidator

from .decorators import accept_transaction
from .models import Record, Sheet, Buyer
from .dictdb import Transaction
from .validators import (
    CustomerOfYourselfValidator, AlreadyAStoreCustomerValidator,
    StoreEmployeeValidator, TransactionExistValidator,
    TransactionSignatureValidator, TransactionStatusValidator,
    IsStoreCustomerValidator, SheetBelongCustomerValidator
)
from .relations import SheetRelatedField


class RecordSerializer(serializers.ModelSerializer):

    transaction = serializers.UUIDField(validators=[
        TransactionExistValidator(),
        TransactionSignatureValidator(),
        TransactionStatusValidator()
    ], write_only=True)

    sheet = SheetRelatedField(read_only=True)
    attendant = ProfileRelatedField()
    signature = ProfileRelatedField(read_only=True)
    store = UserRelatedField(write_only=True, validators=[
        IsStoreCustomerValidator()
    ])

    @atomic
    @accept_transaction
    def create(self, validated_data):
        request = self.context['request']
        store = validated_data.pop('store')
        sheet = request.user.customersheets.get(store=store)
        obj = Record(**validated_data)
        obj.sheet = sheet
        obj.signature = request.user.profile
        obj.save()
        return obj

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = [
            'is_deleted'
        ]
        validators = [
            StoreEmployeeValidator()
        ]


class SheetSerializer(serializers.ModelSerializer):

    transaction = serializers.UUIDField(validators=[
        TransactionExistValidator(),
        TransactionSignatureValidator(),
        TransactionStatusValidator()
    ], write_only=True)

    store = UserRelatedField(validators=[
        CustomerOfYourselfValidator(),
        AlreadyAStoreCustomerValidator()
    ])
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


class BuyerSerializer(serializers.ModelSerializer):

    sheet = SheetRelatedField(validators=[
        SheetBelongCustomerValidator()
    ])

    profile = ProfileRelatedField(validators=[
        ProfileBelongUserValidator()
    ])

    class Meta:
        model = Buyer
        fields = '__all__'


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
        tran = Transaction(str(uuid.uuid4()))
        tran.action = validated_data['action']
        tran.store = request.user.id
        tran.payload = validated_data['payload']
        tran.save(60*30)  # 30 minutes
        return tran.data

    def update(self, instance, validated_data):
        raise NotImplementedError
