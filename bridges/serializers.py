from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    data = serializers.JSONField(
        read_only=True,
        source='datajson')

    class Meta:
        model = Transaction
        fields = '__all__'
