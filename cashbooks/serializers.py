from datetime import timedelta

from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.utils import timezone

from rest_framework import serializers

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from .models import Record, Transaction, AllowedDebtor


class RecordSerializer(serializers.ModelSerializer):

    channel_name = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user
        if user.id != attrs['buyer'].accountable.id:
            message = _('Debtor isn\'t accountable of buyer.')
            raise serializers.ValidationError(message)
        if attrs['creditor'].id != attrs['seller'].accountable.id:
            message = _('Creditor isn\'t accountable of seller.')
            raise serializers.ValidationError(message)
        if user.id == attrs['creditor'].id:
            message = _('Creditor and debtor are the same user.')
            raise serializers.ValidationError(message)
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        channel_name = validated_data.pop('channel_name')
        request = self.context['request']
        obj = Record(**validated_data)
        obj.debtor = request.user
        obj.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(
            channel_name, {
                'type': 'websocket.disconnect',
                'text': 'ACCEPTED',
            },
        )
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
        balance = instance['payment_sum'] - instance['debt_sum']
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
        balance = instance['payment_sum'] - instance['debt_sum']
        return {
            'id': instance['debtor__id'],
            'name': instance['debtor__name'],
            'balance': balance,
        }

    def to_internal_value(self, data):
        pass


class AllowedDebtorSerializer(serializers.ModelSerializer):

    creditor = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = AllowedDebtor
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        obj = Transaction()
        obj.expired_at = timezone.now() + timedelta(days=1)
        obj.save()
        return obj

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('expired_at', 'finished',)
