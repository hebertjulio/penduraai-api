from rest_framework.serializers import CurrentUserDefault
from rest_framework import serializers

from accounts.fields import CurrentProfileDefault

from .db import Ticket


class TicketWriteSerializer(serializers.Serializer):

    scope = serializers.CharField(required=True)
    user = serializers.HiddenField(default=CurrentUserDefault())
    profile = serializers.HiddenField(default=CurrentProfileDefault())
    data = serializers.JSONField(binary=True, default={})
    expire = serializers.IntegerField(required=True)

    def create(self, validated_data):
        ticket = Ticket()
        ticket.scope = validated_data['scope']
        ticket.data = validated_data['data']
        ticket.user = validated_data['user'].id
        ticket.profile = validated_data['profile'].id
        ticket.expire = validated_data['expire']
        return ticket

    def update(self, instance, validated_data):
        raise NotImplementedError


class TicketReadSerializer(serializers.Serializer):

    id = serializers.CharField(read_only=True)
    scope = serializers.CharField(read_only=True)
    user = serializers.IntegerField(read_only=True)
    profile = serializers.IntegerField(read_only=True)
    data = serializers.JSONField(read_only=True)
    expire = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError
