from django.db import models
from django.utils import timezone

class Channel(models.Model):
    CHANNEL_TYPES = (
        ('text', 'Text'),
        ('voice', 'Voice'),
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    channel_type = models.CharField(max_length=10, choices=CHANNEL_TYPES, default='text')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "channels"
        
    def __str__(self):
        return self.name
