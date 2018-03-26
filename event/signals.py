from django.dispatch import receiver
from django.db.models.signals import post_save

from event.models import Event
from event.models import Prize
from notification.models import Notification


@receiver(post_save, sender=Event)
def ensure_prize_exists(sender, instance, created, **kwargs):
    if created is False:
        prize = Prize.objects.filter(event=instance).first()
        if prize is None:
            prize = instance.budget * .8
            prize_set = [Prize(title="First Prize",
                               amount=prize * .5,
                               event=instance,),
                         Prize(title="Second Prize",
                               amount=prize * .3,
                               event=instance,),
                         Prize(title="Third Prize",
                               amount=prize * .2,
                               event=instance,)
                         ]
            Prize.objects.bulk_create(prize_set)


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


@receiver(post_save, sender=Prize)
def prize_notif(sender, instance, created, **kwargs):
    if created is False:
        prize = instance
        if prize.user is not None:
            message = "Congratulations " + prize.user.username + " you won " + prize.title + " in the event " + prize.event.name
            notif = Notification(message=message,
                                 user=prize.user,
                                 )
            notif.save()
