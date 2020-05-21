from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Record, Whitelist


class RecordSerializer(serializers.ModelSerializer):

    def validate_buyer(self, buyer):
        debtor = self.context['request'].user
        if debtor.id != buyer.accountable.id:
            message = _('Debtor isn\'t accountable of buyer.')
            raise serializers.ValidationError(message)
        return buyer

    def validate_seller(self, seller):
        creditor = self.context['request'].data.get('creditor')
        debtor = self.context['request'].user
        if creditor and int(creditor) != debtor.id:
            message = _('Creditor and debtor are same user.')
            raise serializers.ValidationError(message)
        if creditor and int(creditor) != seller.accountable.id:
            message = _('Creditor isn\'t accountable of seller.')
            raise serializers.ValidationError(message)
        return seller

    def create(self, validated_data):
        request = self.context['request']
        obj = Record(**validated_data)
        obj.debtor = request.user
        obj.save()
        return obj

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = ('debtor',)


class CreditorSerializar(serializers.BaseSerializer):

    def create(self, validated_data):
        pass

    def update(self, record, validated_data):
        pass

    def to_representation(self, record):
        balance = record['payments'] - record['debts']
        return {
            'id': record['creditor__id'],
            'name': record['creditor__name'],
            'balance': balance,
        }

    def to_internal_value(self, data):
        pass


class DebtorSerializar(serializers.BaseSerializer):

    def create(self, validated_data):
        pass

    def update(self, record, validated_data):
        pass

    def to_representation(self, record):
        balance = record['payments'] - record['debts']
        return {
            'id': record['debtor__id'],
            'name': record['debtor__name'],
            'balance': balance,
        }

    def to_internal_value(self, data):
        pass


class WhitelistSerializer(serializers.ModelSerializer):

    creditor = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Whitelist
        fields = '__all__'
