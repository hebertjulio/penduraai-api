from rest_framework import serializers
from rest_framework.exceptions import NotFound

from accounts.relations import UserRelatedField, ProfileRelatedField
from accounts.fields import CurrentProfileDefault
from accounts.validators import ProfileBelongUserValidator

from bridges.decorators import use_transaction
from bridges.validators import TransactionSignatureValidator

from .relations import SheetRelatedField
from .models import Record, Sheet

from .validators import (
    CustomerOfYourselfValidator, AlreadyCustomerOfMerchantValidator,
    EmployeeOfMerchantValidator, CustomerOfMerchantValidator,
    SheetBelongCustomerValidator, ProfileCanBuyValidator)


class RecordWriteSerializer(serializers.ModelSerializer):

    signatory = serializers.HiddenField(
        default=CurrentProfileDefault()
    )

    merchant = UserRelatedField(
        validators=[
            CustomerOfMerchantValidator()
        ]
    )

    def get_sheet(self, merchant):
        try:
            request = self.context['request']
            user = request.user
            sheet = merchant.merchantsheets.get(customer=user)
            return sheet
        except Sheet.DoesNotExist:
            raise NotFound

    @use_transaction
    def create(self, validated_data):
        merchant = validated_data.pop('merchant')
        sheet = self.get_sheet(merchant)
        obj = Record(**{**validated_data, **{'sheet': sheet}})
        obj.save()
        return obj

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Record
        exclude = [
            'sheet'
        ]
        validators = [
            EmployeeOfMerchantValidator(),
            ProfileCanBuyValidator(),
            TransactionSignatureValidator()
        ]


class RecordReadSerializer(serializers.ModelSerializer):

    sheet = SheetRelatedField(read_only=True)
    attendant = ProfileRelatedField(read_only=True)

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = [
            f for f in Record.get_fields()
        ]


class SheetWriteSerializer(serializers.ModelSerializer):

    merchant = UserRelatedField(
        validators=[
            CustomerOfYourselfValidator(),
            AlreadyCustomerOfMerchantValidator()
        ]
    )

    customer = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    @use_transaction
    def create(self, validated_data):
        sheet = super().create(validated_data)
        return sheet

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Sheet
        fields = '__all__'
        validators = [
            TransactionSignatureValidator()
        ]


class SheetReadSerializer(serializers.ModelSerializer):

    merchant = UserRelatedField(read_only=True)
    customer = UserRelatedField(read_only=True)
    buyers = ProfileRelatedField(read_only=True, many=True)

    balance = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2
    )

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Sheet
        fields = '__all__'
        read_only_fields = [
            f for f in Sheet.get_fields()
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
