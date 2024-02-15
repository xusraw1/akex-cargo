from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, verbose_name='Username', unique=True)
    first_name = models.CharField(max_length=50, verbose_name='Ism')
    last_name = models.CharField(max_length=50, verbose_name='Familiya')
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(verbose_name='Email Manzil')
    telegram = models.URLField(verbose_name='Telegram', null=True, blank=True)
    akex_id = models.CharField(blank=True, null=True, verbose_name='KARGO ID', max_length=15)
    phone = models.CharField(max_length=15, verbose_name='Telefon Raqam')
    avatar = models.ImageField(upload_to='users/avatars/', default='avatar.png', verbose_name='Avatar')
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,
                               username=instance.username,
                               first_name=instance.first_name,
                               last_name=instance.last_name,
                               email=instance.email)
