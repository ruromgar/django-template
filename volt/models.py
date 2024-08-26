import logging

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

logger = logging.getLogger(__name__)


class Profile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_info = models.JSONField(null=True, blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance: User, created, **kwargs):
    """Create a profile for a user if it does not exist."""
    profile_exists = Profile.objects.filter(user=instance).exists()
    if created and not profile_exists:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


class InviteCode(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=15, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    source_event = models.CharField(max_length=500, null=True, blank=True)
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='created_invite_codes'
    )
    used_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='used_invite_codes'
    )

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(15)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {'Active' if self.is_active else 'Inactive'}"

    def deactivate(self):
        self.is_active = False
        self.save()
