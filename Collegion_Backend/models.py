from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from chat_room.models import ChatRoom


class DMMessage(models.Model):
     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', null=True)
     message = models.CharField(max_length=1200)
     timestamp = models.DateTimeField(auto_now_add=True)
     is_read = models.BooleanField(default=False)

     def __str__(self):
           return self.message
     class Meta:
           ordering = ('timestamp',)


class GroupMessage(models.Model):
    is_read = models.ManyToManyField(User, related_name="is_read_group")
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=1200)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, related_name='chat_room', null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_sender')


    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dm_users = models.ManyToManyField(User, related_name="dm_users")

    # this method called for admin panel
    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
