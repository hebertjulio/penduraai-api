from django.db.transaction import atomic

from rest_framework import serializers

from accounts.relations import UserRelatedField, ProfileRelatedField
from accounts.validators import ProfileBelongUserValidator

from .relations import SheetRelatedField
from .models import Record, Sheet, Buyer
from .validators import (
    CustomerOfYourselfValidator, AlreadyAStoreCustomerValidator,
    StoreEmployeeValidator, IsStoreCustomerValidator,
    SheetBelongCustomerValidator
)


class RecordSerializer(serializers.ModelSerializer):

    sheet = SheetRelatedField(read_only=True)
    attendant = ProfileRelatedField()
    signature = ProfileRelatedField(read_only=True)
    store = UserRelatedField(write_only=True, validators=[
        IsStoreCustomerValidator()
    ])

    @atomic
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
            'is_active'
        ]
        validators = [
            StoreEmployeeValidator()
        ]


class SheetSerializer(serializers.ModelSerializer):

    store = UserRelatedField(validators=[
        CustomerOfYourselfValidator(),
        AlreadyAStoreCustomerValidator()
    ])
    customer = UserRelatedField(read_only=True)

    @atomic
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
