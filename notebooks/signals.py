from django.db.models.signals import post_save
from django.dispatch import receiver

from bridges.services import send_messages

from .models import Record, Sheet


@receiver(post_save, sender=Record)
def record_created(sender, instance, created, **kwargs):
    if created:
        send_messages(instance.transaction)


@receiver(post_save, sender=Sheet)
def sheet_created(sender, instance, created, **kwargs):
    if created:
        send_messages(instance.transaction)
