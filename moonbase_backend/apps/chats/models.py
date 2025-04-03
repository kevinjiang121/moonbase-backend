from django.db import models
from django.utils import timezone
from apps.users.models import User
from apps.channels.models import Channel

class Chat(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='chats')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)
    username = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.username or self.author.username}: {self.content[:50]}"

    class Meta:
        db_table = "chats"