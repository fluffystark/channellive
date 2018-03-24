from django.dispatch import receiver
from django.db.models.signals import post_save

from event.models import Event
from notification.models import Notification


@receiver(post_save, sender=Event)
def approved_notif(sender, instance, created, **kwargs):
    if created is False:
        event = instance
        if event.review == Event.APPROVED:
            message = "Your event named " + event.name + " has been approved."
            notif = Notification(message=message,
                                 user=event.business.user,
                                 )
            notif.save()
