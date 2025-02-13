from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Profile 객체가 있는지 확인 후 저장 (에러 방지를 위한 조건 추가)
    if hasattr(instance, 'profile'):
        instance.profile.save()