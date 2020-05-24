from rest_framework import serializers

from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        obj = User(**validated_data)
        obj.is_active = True
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


class ProfileSerializer(serializers.ModelSerializer):

    accountable = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileAuthenticateSerializer(serializers.Serializer):

    accountable = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
