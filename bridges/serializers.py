from rest_framework import serializers

from .db import Ticket


class TicketSerializer(serializers.Serializer):

    scope = serializers.CharField(required=True)
    expire = serializers.IntegerField(required=True)
    status = serializers.CharField(read_only=True)
    data = serializers.JSONField(binary=True, required=True)
    token = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs):
        exclude = kwargs.pop('exclude', [])
        super().__init__(*args, **kwargs)
        for field in exclude:
            del self.fields[field]

    def create(self, validated_data):
        ticket = Ticket()
        ticket.scope = validated_data['scope']
        ticket.data = validated_data['data']
        ticket.status = 'unused'
        ticket.expire = validated_data['expire']
        return ticket

    def update(self, instance, validated_data):
        raise NotImplementedError
