from django.dispatch import receiver
from django.db.models.signals import post_save

from event.models import Event
from event.models import Prize


# @receiver(post_save, sender=Event)
# def approved_notif(sender, instance, created, **kwargs):
#     if created is True:
#         prize = instance.budget * .8
#         prize_set = [Prize(title="First Prize",
#                            amount=prize * .5,
#                            event=instance,),
#                      Prize(title="Second Prize",
#                            amount=prize * .3,
#                            event=instance,),
#                      Prize(title="Third Prize",
#                            amount=prize * .2,
#                            event=instance,)
#                      ]
#         Prize.objects.bulk_create(prize_set)


@receiver(post_save, sender=Event)
def ensure_prize_exists(sender, instance, created, **kwargs):
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
