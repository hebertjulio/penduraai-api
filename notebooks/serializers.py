from rest_framework import serializers
from rest_framework.exceptions import NotFound

from accounts.relations import UserRelatedField, ProfileRelatedField
from accounts.fields import CurrentProfileDefault
from accounts.validators import ProfileBelongUserValidator

from bridges.decorators import new_transaction

from .relations import SheetRelatedField
from .models import Record, Sheet
from .validators import (
    CustomerOfYourselfValidator, AlreadyCustomerOfMerchantValidator,
    EmployeeOfMerchantValidator, CustomerOfMerchantValidator,
    SheetBelongCustomerValidator, ProfileCanBuyValidator
)


class RecordRequestSerializer(serializers.ModelSerializer):

    transaction = serializers.IntegerField(read_only=True)

    attendant = serializers.HiddenField(
        default=CurrentProfileDefault(),
        write_only=True
    )

    merchant = UserRelatedField(
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
            'merchant', 'attendant', 'value',
            'operation', 'note', 'transaction'
        ]
        extra_kwargs = {
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
    attendant = ProfileRelatedField()

    merchant = UserRelatedField(
        validators=[
            CustomerOfMerchantValidator()
        ],
        write_only=True
    )

    @classmethod
    def get_sheet(cls, merchant, user):
        try:
            sheet = merchant.merchantsheets.get(customer=user)
            return sheet
        except Sheet.DoesNotExist:
            raise NotFound

    def create(self, validated_data):
        merchant = validated_data.pop('merchant')
        request = self.context['request']
        sheet = self.get_sheet(merchant, request.user)
        validated_data.update({
            'sheet': sheet, 'signatory': request.profile
        })
        obj = super().create(validated_data)
        return obj

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = [
            'is_active', 'signatory'
        ]
        validators = [
            EmployeeOfMerchantValidator(),
            ProfileCanBuyValidator()
        ]


class RecordListSerializer(serializers.ModelSerializer):

    sheet = SheetRelatedField()
    attendant = ProfileRelatedField()

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Record
        fields = '__all__'


class RecordDetailSerializer(serializers.ModelSerializer):

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


class SheetRequestSerializer(serializers.ModelSerializer):

    transaction = serializers.IntegerField(read_only=True)

    merchant = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    @new_transaction(scope='sheet')
    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Sheet
        fields = [
            'transaction', 'merchant'
        ]


class SheetCreateSerializer(serializers.ModelSerializer):

    merchant = UserRelatedField(
        validators=[
            CustomerOfYourselfValidator(),
            AlreadyCustomerOfMerchantValidator()
        ]
    )

    customer = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Sheet
        fields = '__all__'


class SheetListSerializer(serializers.ModelSerializer):

    merchant = UserRelatedField()
    customer = UserRelatedField()
    buyers = ProfileRelatedField(many=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Sheet
        fields = '__all__'


class SheetDetailSerializer(serializers.ModelSerializer):

    buyers = ProfileRelatedField(many=True, read_only=True)

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
