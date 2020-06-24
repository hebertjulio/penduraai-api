from rest_framework import serializers
from rest_framework.exceptions import NotFound

from accounts.relations import UserRelatedField, ProfileRelatedField
from accounts.fields import CurrentProfileDefault
from accounts.validators import ProfileBelongUserValidator

from bridges.decorators import new_transaction

from .relations import SheetRelatedField
from .models import Record, Sheet, Buyer
from .validators import (
    CustomerOfYourselfValidator, AlreadyAStoreCustomerValidator,
    StoreEmployeeValidator, IsStoreCustomerValidator,
    SheetBelongCustomerValidator
)


class RecordRequestSerializer(serializers.ModelSerializer):

    transaction = serializers.IntegerField(read_only=True)

    store = UserRelatedField(
        default=serializers.CurrentUserDefault(),
        write_only=True
    )

    @new_transaction(scope='record')
    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Record
        fields = [
            'store', 'attendant', 'value',
            'operation', 'note', 'transaction'
        ]
        extra_kwargs = {
            'attendant': {
                'default': CurrentProfileDefault(),
                'write_only': True
            },
            'note': {
                'write_only': True
            },
            'value': {
                'write_only': True
            },
            'operation': {
                'write_only': True
            }
        }


class RecordCreateSerializer(serializers.ModelSerializer):

    sheet = SheetRelatedField(read_only=True)
    attendant = ProfileRelatedField(read_only=True)

    signature = ProfileRelatedField(
        default=CurrentProfileDefault(),
        read_only=True
    )

    store = UserRelatedField(
        validators=[
            IsStoreCustomerValidator()
        ],
        write_only=True
    )

    @classmethod
    def get_sheet(cls, store, user):
        try:
            sheet = store.storesheets.get(customer=user)
            return sheet
        except Sheet.DoesNotExist:
            raise NotFound

    def create(self, validated_data):
        store = validated_data.pop('store')
        request = self.context['request']
        sheet = self.get_sheet(store, request.user)
        validated_data.update({'sheet': sheet})
        obj = super().create(validated_data)
        return obj

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = [
            'is_active'
        ]
        validators = [
            StoreEmployeeValidator()
        ]


class RecordReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = [
            f for f in Record.get_fields()
        ]
        validators = [
            StoreEmployeeValidator()
        ]


class SheetRequestSerializer(serializers.ModelSerializer):

    transaction = serializers.IntegerField(read_only=True)

    @new_transaction(scope='sheet')
    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Sheet
        fields = [
            'store', 'transaction'
        ]
        extra_kwargs = {
            'store': {
                'default': serializers.CurrentUserDefault(),
                'write_only': True
            }
        }


class SheetCreateSerializer(serializers.ModelSerializer):

    store = UserRelatedField(
        validators=[
            CustomerOfYourselfValidator(),
            AlreadyAStoreCustomerValidator()
        ]
    )

    customer = UserRelatedField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Sheet
        fields = [
            'store', 'customer'
        ]


class SheetReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sheet
        fields = '__all__'
        read_only_fields = [
            f for f in Record.get_fields()
        ]


class BuyerSerializer(serializers.ModelSerializer):

    sheet = SheetRelatedField(
        validators=[SheetBelongCustomerValidator()])

    profile = ProfileRelatedField(
        validators=[ProfileBelongUserValidator()])

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
            'balance': instance['balance']
        }

    def to_internal_value(self, data):
        raise NotImplementedError
