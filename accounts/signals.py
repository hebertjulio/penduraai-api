from random import randint

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Profile


@receiver(post_save, sender=User)
def owner_profile(sender, instance, created, **kwargs):
    if not created:
        try:
            obj = instance.userprofiles.get(role=Profile.ROLE.owner)
        except Profile.DoesNotExist:
            pass
        else:
            if obj.name != instance.name:
                obj.name = instance.name
                obj.save()
