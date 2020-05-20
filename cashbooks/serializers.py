from rest_framework import serializers

from accounts.fields import ProfileField
from accounts.serializers import UserSerializer

from .models import Transaction


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


class CreditorSerializar(serializers.Serializer):

    creditor = UserSerializer(read_only=True)


class DebtorSerializar(serializers.Serializer):

    debtor = UserSerializer(read_only=True)
