from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
<<<<<<< HEAD
    if hasattr(instance, 'profile'):
        instance.profile.save()
=======
    instance.profile.save()
>>>>>>> 41ed5fd5187ab39341d77cca20e710c0fa006da1
