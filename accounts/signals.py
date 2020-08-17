from random import randint

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Profile


@receiver(post_save, sender=User)
def owner_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        pin = getattr(user, 'pin', randint(1111, 9999))  # nosec
        profile = Profile(**{
            'name': user.name, 'pin': pin, 'user': user,
            'role': Profile.ROLE.owner})
        profile.save()
