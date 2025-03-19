from django.db import models
from django.utils import timezone

class ChannelGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "channel_groups"


class Channel(models.Model):
    CHANNEL_TYPES = (
        ('text', 'Text'),
        ('voice', 'Voice'),
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    channel_type = models.CharField(max_length=10, choices=CHANNEL_TYPES, default='text')
    group = models.ForeignKey(
        ChannelGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="channels"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "channels"
