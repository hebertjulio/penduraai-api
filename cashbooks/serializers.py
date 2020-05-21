from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Record, Whitelist


class RecordSerializer(serializers.ModelSerializer):

    def validate_buyer(self, value):
        debtor = self.context['request'].user
        if debtor.id != value.accountable.id:
            message = _('Debtor isn\'t accountable of buyer.')
            raise serializers.ValidationError(message)
        return value

    def validate_seller(self, value):
        creditor = self.context['request'].data.get('creditor')
        if creditor and int(creditor) != value.accountable.id:
            message = _('Creditor isn\'t accountable of seller.')
            raise serializers.ValidationError(message)
        return value

    def validate(self, data):
        creditor = self.context['request'].data.get('creditor')
        debtor = self.context['request'].user
        if creditor and int(creditor) == debtor.id:
            message = _('Creditor and debtor are the same user.')
            raise serializers.ValidationError(message)
        return data

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

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        balance = instance['payments'] - instance['sales']
        return {
            'id': instance['creditor__id'],
            'name': instance['creditor__name'],
            'balance': balance,
        }

    def to_internal_value(self, data):
        pass


class DebtorSerializar(serializers.BaseSerializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        balance = instance['payments'] - instance['sales']
        return {
            'id': instance['debtor__id'],
            'name': instance['debtor__name'],
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
