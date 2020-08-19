from datetime import timedelta
from json import dumps

from django.utils import timezone
from django.db.models import Model

from rest_framework import serializers

from .models import Ticket


class TicketWriteSerializer(serializers.ModelSerializer):

    expire_in = serializers.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        serializer = kwargs.pop('serializer')
        super().__init__(*args, **kwargs)
        if serializer:
            self.fields['payload'] = serializer

    def create(self, validated_data):
        expire_in = validated_data.pop('expire_in')
        expire_at = timezone.now() + timedelta(minutes=expire_in)
        items = validated_data['payload'].items()
        payload = dumps({
            k: v.id if isinstance(v, Model) else v for k, v in items})
        validated_data.update({'payload': payload, 'expire_at': expire_at})
        ticket = super().create(validated_data)
        return ticket

    class Meta:
        model = Ticket
        exclude = [
            'expire_at', 'usage'
        ]


class TicketReadSerializer(serializers.ModelSerializer):

    payload = serializers.JSONField(read_only=True, source='payload_as_dict')
    token = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs):
        exclude = kwargs.pop('exclude', [])
        super().__init__(*args, **kwargs)
        for field in exclude:
            self.fields.pop(field)

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = [
            f for f in Ticket.get_fields()
        ]
