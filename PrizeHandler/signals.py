from django.dispatch import receiver
from django.db.models.signals import post_save

from event.models import Event
from PrizeHandler.models import Prize


@receiver(post_save, sender=Event)
def ensure_prize_exists(sender, instance, created, **kwargs):
    print "hello"
    if created is False:
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
