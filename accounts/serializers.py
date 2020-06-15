from django.db.transaction import atomic

from rest_framework import serializers

from .models import User, Profile
from .validators import (
    AccountablePINUniqueTogetherValidator, RoleOwnerValidator
)


class UserCreateSerializer(serializers.ModelSerializer):

    pin = serializers.RegexField(regex=Profile.PIN_REGEX, write_only=True)

    @atomic
    def create(self, validated_data):
        pin = validated_data.pop('pin')
        user = User(**validated_data)
        user.is_active = True
        user.set_password(validated_data['password'])
        user.save()
        # create owner profile
        profile = Profile(**{
            'name': user.name, 'pin': pin, 'accountable': user,
            'role': Profile.ROLE.owner,
            'can_attend': True, 'can_buy': True
        })
        profile.save()
        return user

    def update(self, instance, validated_data):
        pass

    class Meta:
        model = User
        exclude = [
            'user_permissions', 'groups', 'is_superuser',
            'is_staff'
        ]
        read_only_fields = [
            'id', 'is_active', 'last_login', 'created',
            'modified'
        ]


class UserUpdateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        raise NotImplementedError

    @atomic
    def update(self, instance, validated_data):
        user = instance
        # change owner profile name when user change its name
        if 'name' in validated_data and user.name != validated_data['name']:
            profile = user.profiles.get(role=Profile.ROLE.owner)
            profile.name = validated_data['name']
            profile.save()
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
            'id', 'is_active', 'last_login', 'created',
            'modified'
        ]


class UserReadSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = User
        exclude = [
            'user_permissions', 'groups', 'is_superuser',
            'is_staff', 'password'
        ]
        read_only_fields = [
            f for f in User.get_fields()
        ]


class ProfileSerializer(serializers.ModelSerializer):

    accountable = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Profile
        fields = '__all__'
        validators = [
            AccountablePINUniqueTogetherValidator()
        ]
        extra_kwargs = {
            'role': {
                'validators': [
                    RoleOwnerValidator()
                ]
            }
        }
