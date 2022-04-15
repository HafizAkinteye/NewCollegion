from django.db import models
from django.contrib.auth.models import User
import datetime

class ChatRoom(models.Model):
    name = models.CharField(max_length=50, null=True)
    create_date = models.DateField(default=datetime.date.today)
    member = models.ManyToManyField(User, related_name="member")
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="creator")
