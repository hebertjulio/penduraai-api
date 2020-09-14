from django.db.transaction import atomic

from rest_framework import serializers
from rest_framework.exceptions import NotFound

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Profile
from .validators import ProfileOwnerRoleValidator


class UserWriteSerializer(serializers.ModelSerializer):

    pin = serializers.RegexField(regex=Profile.PIN_REGEX, write_only=True)

    @atomic
    def create(self, validated_data):
        pin = validated_data.pop('pin')
        user = User(**validated_data)
        user.is_active = True
        user.pin = pin
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = instance
        password = validated_data.pop('password', None)
        if password:
            user.set_password(password)
        user = super().update(user, validated_data)
        return user

    class Meta:
        model = User
        exclude = [
            'user_permissions', 'groups', 'is_superuser',
            'is_staff'
        ]
        read_only_fields = [
            'is_active', 'last_login'
        ]


class UserReadSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = User
        read_only_fields = User.get_fields()
        exclude = [
            'password', 'groups', 'user_permissions'
        ]


class ProfileWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            'role': {
                'validators': [
                    ProfileOwnerRoleValidator()
                ]
            },
        }


class ProfileReadSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Profile
        read_only_fields = User.get_fields()
        exclude = [
            'pin'
        ]


class ProfileUnlockSerializer(serializers.Serializer):

    id = serializers.IntegerField(write_only=True)
    pin = serializers.RegexField(regex=Profile.PIN_REGEX, write_only=True)
    access = serializers.CharField(read_only=True)

    def validate(self, validated_data):
        try:
            user = self.context['request'].user
            profile = user.userprofiles.get(
                id=validated_data['id'], pin=validated_data['pin'])
            refresh = RefreshToken()
            refresh[api_settings.USER_ID_CLAIM] = user.id
            refresh['profile_id'] = profile.id
            return {'access': refresh.access_token}
        except Profile.DoesNotExist:
            raise NotFound
