from datetime import timedelta
from json import dumps

from django.utils import timezone

from rest_framework import serializers

from .models import Transaction


class TransactionWriteSerializer(serializers.ModelSerializer):

    data = serializers.JSONField(binary=True, required=True)
    expire_in = serializers.IntegerField(required=True)

    def create(self, validated_data):
        expire_in = validated_data.pop('expire_in')
        expire_at = timezone.now() + timedelta(minutes=expire_in)
        data = dumps(validated_data['data'])
        validated_data.update({'data': data, 'expire_at': expire_at})
        transaction = super().create(validated_data)
        return transaction

    class Meta:
        model = Transaction
        exclude = [
            'expire_at'
        ]


class TransactionReadSerializer(serializers.ModelSerializer):

    data = serializers.JSONField(read_only=True, source='data_as_dict')
    token = serializers.CharField(read_only=True)
    expired = serializers.BooleanField(read_only=True)

    def __init__(self, *args, **kwargs):
        exclude = kwargs.pop('exclude', [])
        super().__init__(*args, **kwargs)
        for field in exclude:
            self.fields.pop(field)

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = [
            f for f in Transaction.get_fields()
        ]
