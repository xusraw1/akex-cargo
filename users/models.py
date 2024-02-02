from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, blank=True, null=True, verbose_name='Username')
    first_name = models.CharField(max_length=50, verbose_name='Ism')
    last_name = models.CharField(max_length=50, verbose_name='Familiya')
    email = models.EmailField(verbose_name='Email Manzil')
    akex_id = models.IntegerField(blank=True, null=True, verbose_name='KARGO ID')
    phone = models.CharField(max_length=15, verbose_name='Telefon Raqam')
    pinfl = models.CharField(max_length=14, null=True, verbose_name='PINFL Raqam')
    sp = models.CharField(max_length=7, blank=True, verbose_name='Pasport Seriya')
    avatar = models.ImageField(upload_to='users/avatars/', default='avatar.png', verbose_name='Avatar')
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return f"{self.akex_id} - {self.first_name.title()} {self.last_name.title()}"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
