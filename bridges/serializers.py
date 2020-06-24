from rest_framework import serializers

from .models import Transaction


class TransactionReadSerializer(serializers.ModelSerializer):

    data = serializers.JSONField(read_only=True, source='json')

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = [
            f for f in Transaction.get_fields()
        ]
