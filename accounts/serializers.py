from django.db.transaction import atomic

from rest_framework import serializers

from bridges.services import new_transaction

from .models import User, Profile
from .validators import ProfileOwnerRoleValidator


class SignUpSerializer(serializers.ModelSerializer):

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
            'name': user.name, 'pin': pin, 'user': user,
            'role': Profile.ROLE.owner
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


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        raise NotImplementedError

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
            'id', 'is_active', 'last_login', 'created',
            'modified'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class ProfileRequestSerializer(serializers.ModelSerializer):

    transaction = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        profile = user.profile
        validated_data['user'] = user
        obj = new_transaction('profile', user, profile, validated_data)
        return {'transaction': obj.id}

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta:
        model = Profile
        fields = [
            'role', 'transaction'
        ]
        extra_kwargs = {
            'role': {
                'write_only': True,
                'validators': [
                    ProfileOwnerRoleValidator()
                ]
            }
        }


class ProfileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = [
            'id', 'created', 'modified'
        ]
        extra_kwargs = {
            'role': {
                'validators': [
                    ProfileOwnerRoleValidator()
                ]
            }
        }


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = [
            'id', 'user', 'created', 'modified'
        ]
        extra_kwargs = {
            'role': {
                'validators': [
                    ProfileOwnerRoleValidator()
                ]
            }
        }
