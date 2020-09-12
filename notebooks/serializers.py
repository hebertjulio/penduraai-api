from rest_framework import serializers

from accounts.relations import UserRelatedField, ProfileRelatedField
from accounts.fields import CurrentProfileDefault
from accounts.validators import ProfileBelongUserValidator

from .relations import SheetRelatedField
from .models import Record, Sheet

from .validators import (
    CustomerOfYourselfValidator, AlreadyCustomerOfMerchantValidator,
    EmployeeOfMerchantValidator, CustomerOfMerchantValidator,
    SheetBelongCustomerValidator, ProfileCanBuyValidator
)


class RecordWriteSerializer(serializers.ModelSerializer):

    signatary = serializers.HiddenField(
        default=CurrentProfileDefault()
    )

    def create(self, validated_data):
        obj = super().create(validated_data)
        return obj

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Record
        fields = '__all__'
        extra_kwargs = {
            'sheet': {
                'validators': [
                    CustomerOfYourselfValidator(),
                    CustomerOfMerchantValidator()
                ]
            }
        }
        validators = [
            EmployeeOfMerchantValidator(),
            ProfileCanBuyValidator()
        ]


class RecordReadSerializer(serializers.ModelSerializer):

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

    merchant = UserRelatedField(
        validators=[
            CustomerOfYourselfValidator(),
            AlreadyCustomerOfMerchantValidator()
        ]
    )

    customer = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def create(self, validated_data):
        sheet = super().create(validated_data)
        return sheet

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Sheet
        fields = '__all__'


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
        read_only_fields = Sheet.get_fields()


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
