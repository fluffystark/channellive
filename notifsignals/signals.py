from django.dispatch import receiver
from django.db.models.signals import post_save

from OpenTokHandler.models import Report
from notification.models import Notification
from user_profile.models import UserProfile


@receiver(post_save, sender=Report)
def report_notif(sender, instance, created, **kwargs):
    if created is True:
        report = instance
        message = "Your Livestream has been reported."
        notif = Notification(message=message,
                             user=report.livestream.user)
        notif.save()


@receiver(post_save, sender=UserProfile)
def newuser_notif(sender, instance, created, **kwargs):
    if created is True:
        userprofile = instance
        message = "Start creating your profile."
        notif = Notification(message=message,
                             user=userprofile.user)
        notif.save()
