from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import  Answer


@receiver(post_save, sender=Answer)
def set_is_done_exercise(sender, instance, created, **kwargs):
    if created:
        instance.is_done_exercise = True
        instance.save()
