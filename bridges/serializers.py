from datetime import timedelta
from json import dumps

from django.utils import timezone
from django.db.models import Model

from rest_framework import serializers

from .models import Ticket


class TicketWriteSerializer(serializers.ModelSerializer):

    expire_in = serializers.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        payload_serializer = kwargs.pop('payload_serializer')
        super().__init__(*args, **kwargs)
        if payload_serializer:
            self.fields['payload'] = payload_serializer

    @classmethod
    def get_valid_payload(cls, items):
        value = {k: v.id if isinstance(v, Model) else v for k, v in items}
        value = dumps(value)
        return value

    def create(self, validated_data):
        expire_in = validated_data.pop('expire_in')
        expire_at = timezone.now() + timedelta(minutes=expire_in)
        items = validated_data['payload'].items()
        payload = self.get_valid_payload(items)
        validated_data.update({'payload': payload, 'expire_at': expire_at})
        ticket = super().create(validated_data)
        return ticket

    class Meta:
        model = Ticket
        exclude = [
            'expire_at', 'usage', 'scope'
        ]


class TicketReadSerializer(serializers.ModelSerializer):

    payload = serializers.JSONField(read_only=True, source='payload_as_dict')
    token = serializers.CharField(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = [
            f for f in Ticket.get_fields()
        ]
