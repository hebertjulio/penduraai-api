from rest_framework import serializers

from accounts.fields import CurrentProfileDefault

from .models import Transaction


class TransactionWriteSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    profile = serializers.HiddenField(default=CurrentProfileDefault())
    data = serializers.JSONField(binary=True, required=True)

    class Meta:
        model = Transaction
        exclude = [
            'scope', 'expire_at'
        ]


class TransactionReadSerializer(serializers.ModelSerializer):

    ttl = serializers.IntegerField(read_only=True)
    expired = serializers.BooleanField(read_only=True)
    used = serializers.BooleanField(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = [
            f for f in Transaction.get_fields()
        ]
