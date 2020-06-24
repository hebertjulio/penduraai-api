from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Profile


@receiver(post_save, sender=User)
def owner_profile_name_update(sender, instance, created, **kwargs):
    """ Change owner profile name when user name is changed """
    if created:
        return
    try:
        profile = instance.userprofiles.get(role=Profile.ROLE.owner)
        if profile.name == instance.name:
            return
        profile.name = instance.name
        profile.save()
    except Profile.DoesNotExist:
        pass
