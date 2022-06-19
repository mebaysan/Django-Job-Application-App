from django.db.models.signals import post_save
from django.contrib.auth.models import User, Permission
from django.dispatch import receiver

from .models import CandidateProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # if user is not a staff, create a candidate profile for the user
    if created and not instance.is_staff:
        CandidateProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if not instance.is_staff:
        instance.candidate_profile.save()


@receiver(post_save, sender=User)
def set_base_candidate_permissions(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        instance.user_permissions.set(
            [
                *Permission.objects.filter(name__contains="Candidate Profile").all(),
                *Permission.objects.filter(name__contains="Job Post").all(),
                *Permission.objects.filter(name__contains="Job Skill").all(),
            ]
        )
        instance.save()
