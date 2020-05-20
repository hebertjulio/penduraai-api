from rest_framework import serializers

from .validators import ProfileOf
from .models import Profile


class ProfileField(serializers.PrimaryKeyRelatedField):

    queryset = Profile.objects.all()
    validators = [ProfileOf()]
