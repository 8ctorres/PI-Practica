from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from jsonfield import JSONField

class SingleIndicatorChart(models.Model):
    indicator = models.CharField(default="Life expectancy", null=False)
    countries = JSONField(null=True)

class MultipleIndicatorChart(models.Model):
    country = models.CharField(default="Spain", null=False)
    indicators = JSONField(null=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    single_indicator = models.OneToOneField(SingleIndicatorChart)
    multiple_indicators = models.ManyToManyField(MultipleIndicatorChart)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()