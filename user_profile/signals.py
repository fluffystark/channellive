from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from user_profile.models import UserProfile



@receiver(post_save, sender=User)
def ensure_user_profile_exists(sender, instance, created, **kwargs):
    if created is True:
        UserProfile.objects.get_or_create(user=instance)
