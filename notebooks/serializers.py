from rest_framework import serializers

from accounts.relations import UserRelatedField, ProfileRelatedField
from accounts.fields import CurrentProfileDefault
from accounts.validators import ProfileBelongUserValidator

from bridges.decorators import create_transaction

from .relations import SheetRelatedField
from .models import Record, Sheet

from .validators import (
    SheetBelongCustomerValidator, ProfileCanBuyValidator,
    CustomerOfMerchantValidator, UserAlreadyCustomerValidator,
    CustomerYourselfValidator, EmployeeOfMerchantValidator
)


class RecordCreateSerializer(serializers.ModelSerializer):

    merchant = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    attendant = ProfileRelatedField(
        validators=[EmployeeOfMerchantValidator()])

    @create_transaction(expire=1800, scope='record')
    def create(self, validated_data):
        return validated_data

    class Meta:
        model = Record
        exclude = [
            'sheet', 'signatary'
        ]


class RecordConfirmSerializer(serializers.ModelSerializer):

    merchant = UserRelatedField(
        validators=[CustomerOfMerchantValidator(), ProfileCanBuyValidator()])

    signatary = serializers.HiddenField(default=CurrentProfileDefault())

    def create(self, validated_data):
        merchant = validated_data.pop('merchant')
        request = self.context['request']
        sheet = merchant.merchantsheets.get(customer=request.user)
        validated_data.update({'sheet': sheet})
        return super().create(validated_data)

    class Meta:
        model = Record
        exclude = [
            'sheet'
        ]


class RecordReadSerializer(serializers.ModelSerializer):

    transaction = serializers.UUIDField(read_only=True)
    sheet = SheetRelatedField(read_only=True)
    attendant = ProfileRelatedField(read_only=True)
    signatary = ProfileRelatedField(read_only=True)

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = Record.get_fields()


class SheetCreateSerializer(serializers.ModelSerializer):

    merchant = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    @create_transaction(expire=1800, scope='sheet')
    def create(self, validated_data):
        return validated_data

    class Meta:
        model = Sheet
        exclude = [
            'customer'
        ]


class SheetConfirmSerializer(serializers.ModelSerializer):

    merchant = UserRelatedField(
        validators=[
            UserAlreadyCustomerValidator(), CustomerYourselfValidator()],
        default=serializers.CurrentUserDefault())

    customer = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Sheet
        fields = '__all__'


class SheetUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sheet
        fields = [
            'is_active'
        ]


class SheetReadSerializer(serializers.ModelSerializer):

    transaction = serializers.UUIDField(read_only=True)
    merchant = UserRelatedField(read_only=True)
    customer = UserRelatedField(read_only=True)

    balance = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Sheet
        read_only_fields = Sheet.get_fields()
        exclude = [
            'profiles'
        ]


class SheetByProfileSerializer(serializers.ModelSerializer):

    merchant = UserRelatedField(read_only=True)
    customer = UserRelatedField(read_only=True)
    can_buy = serializers.BooleanField(read_only=True)

    class Meta:
        model = Sheet
        read_only_fields = Sheet.get_fields()
        exclude = [
            'profiles'
        ]


class SheetProfileAddSerializer(serializers.Serializer):

    sheet = SheetRelatedField(
        validators=[SheetBelongCustomerValidator()])

    profile = ProfileRelatedField(
        validators=[ProfileBelongUserValidator()])

    def create(self, validated_data):
        sheet = validated_data['sheet']
        sheet.profiles.add(validated_data['profile'])
        return validated_data
