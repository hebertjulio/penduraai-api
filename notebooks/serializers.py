from rest_framework import serializers

from accounts.relations import UserRelatedField, ProfileRelatedField
from accounts.fields import CurrentProfileDefault
from accounts.validators import ProfileBelongUserValidator

from bridges.decorators import create_transaction

from .relations import SheetRelatedField
from .models import Record, Sheet

from .validators import (
    EmployeeOfMerchantValidator, SheetBelongCustomerValidator,
    ProfileCanBuyValidator
)


class RecordWriteSerializer(serializers.ModelSerializer):

    merchant = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    attendant = serializers.HiddenField(
        default=CurrentProfileDefault()
    )

    @create_transaction(expire=1800, scope='record')
    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Record
        exclude = [
            'sheet', 'signatary'
        ]
        validators = [
            EmployeeOfMerchantValidator(),
            ProfileCanBuyValidator()
        ]


class RecordReadSerializer(serializers.ModelSerializer):

    transaction = serializers.UUIDField(read_only=True)
    sheet = SheetRelatedField(read_only=True)
    attendant = ProfileRelatedField(read_only=True)
    signatary = ProfileRelatedField(read_only=True)

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = Record.get_fields()


class SheetWriteSerializer(serializers.ModelSerializer):

    merchant = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    @create_transaction(expire=1800, scope='sheet')
    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Sheet
        exclude = [
            'customer'
        ]


class SheetReadSerializer(serializers.ModelSerializer):

    transaction = serializers.UUIDField(read_only=True)
    merchant = UserRelatedField(read_only=True)
    customer = UserRelatedField(read_only=True)

    balance = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2
    )

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Sheet
        read_only_fields = Sheet.get_fields()
        exclude = [
            'buyers'
        ]


class SheetProfileAddSerializer(serializers.Serializer):

    sheet = SheetRelatedField(
        validators=[
            SheetBelongCustomerValidator()
        ]
    )

    profile = ProfileRelatedField(
        validators=[
            ProfileBelongUserValidator()
        ]
    )

    def create(self, validated_data):
        sheet = validated_data['sheet']
        sheet.buyers.add(validated_data['profile'])
        return validated_data

    def update(self, instance, validated_data):
        raise NotImplementedError
