from django.db.transaction import atomic

from rest_framework import serializers

from bridges.decorators import use_transaction
from bridges.fields import TransactionTokenField

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
        exclude = [
            'password', 'groups', 'user_permissions'
        ]
        read_only_fields = [
            f for f in User.get_fields()
        ]


class ProfileWriteSerializer(serializers.ModelSerializer):

    transaction = TransactionTokenField(required=True)

    @use_transaction
    def create(self, validated_data):
        profile = super().create(validated_data)
        return profile

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
        fields = '__all__'
        read_only_fields = [
            f for f in User.get_fields()
        ]


class ProfileScopeSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Profile
        fields = [
            'user', 'role'
        ]
