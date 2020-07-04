from random import randint

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Profile


@receiver(post_save, sender=User)
def owner_profile(sender, instance, created, **kwargs):
    if not created:
        try:
            obj = instance.userprofiles.get(role=Profile.ROLE.owner)
            if obj.name != instance.name:
                obj.name = instance.name
                obj.save()
        except Profile.DoesNotExist:
            pass
    else:
        pin = randint(1000, 9999)  # nosec
        obj = Profile(**{
            'name': instance.name, 'pin': pin,
            'role': Profile.ROLE.owner, 'user': instance})
        obj.save()
