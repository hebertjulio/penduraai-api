from datetime import timedelta
from json import dumps

from django.utils import timezone
from django.db.models import Model

from rest_framework import serializers

from .models import Transaction


class TransactionWriteSerializer(serializers.ModelSerializer):

    expire_in = serializers.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        serializer = kwargs.pop('serializer')
        super().__init__(*args, **kwargs)
        if serializer:
            self.fields['data'] = serializer

    def create(self, validated_data):
        expire_in = validated_data.pop('expire_in')
        expire_at = timezone.now() + timedelta(minutes=expire_in)
        items = validated_data['data'].items()
        data = dumps({
            k: v.id if isinstance(v, Model) else v for k, v in items})
        validated_data.update({'data': data, 'expire_at': expire_at})
        transaction = super().create(validated_data)
        return transaction

    class Meta:
        model = Transaction
        exclude = [
            'expire_at', 'usage'
        ]


class TransactionReadSerializer(serializers.ModelSerializer):

    data = serializers.JSONField(read_only=True, source='data_as_dict')
    token = serializers.CharField(read_only=True)

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
