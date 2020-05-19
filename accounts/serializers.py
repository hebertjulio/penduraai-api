from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        obj = User(**validated_data)
        obj.is_active = False
        obj.set_password(validated_data['password'])
        obj.save()
        return obj

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = User
        exclude = [
            'user_permissions', 'groups', 'is_superuser', 'is_staff']
        read_only_fields = [
            'id', 'is_active', 'last_login', 'created', 'modified']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
