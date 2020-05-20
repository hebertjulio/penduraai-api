from rest_framework import serializers

from accounts.fields import ProfileField
from accounts.serializers import UserSerializer

from .models import Transaction, Whitelist


class TransactionSerializer(serializers.ModelSerializer):

    requester = ProfileField()
    subscriber = ProfileField()

    def create(self, validated_data):
        request = self.context['request']
        obj = Transaction(**validated_data)
        obj.debtor = request.user
        obj.save()
        return obj

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('debtor',)


class CreditorSerializar(serializers.BaseSerializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        serializer = UserSerializer(instance.creditor)
        return {
            'debit_sum': instance.debit_sum,
            'credit_sum': instance.credit_sum,
            'user': serializer.data,
        }

    def to_internal_value(self, data):
        pass


class DebtorSerializar(serializers.BaseSerializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        serializer = UserSerializer(instance.debtor)
        return {
            'debit_sum': instance.debit_sum,
            'credit_sum': instance.credit_sum,
            'user': serializer.data,
        }

    def to_internal_value(self, data):
        pass


class WhitelistSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Whitelist
        fields = '__all__'
