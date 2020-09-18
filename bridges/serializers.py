from rest_framework import serializers


class TransactionReadSerializer(serializers.Serializer):

    id = serializers.CharField(read_only=True)
    expire = serializers.IntegerField(read_only=True)
    data = serializers.JSONField(read_only=True)
    scope = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError
