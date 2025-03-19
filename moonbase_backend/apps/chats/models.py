from django.db import models
from django.utils import timezone
from apps.users.models import User
from apps.channels.models import Channel

class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "chats"

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}"
