from django.db import models
from django.utils import timezone

class User(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('mod', 'Moderator'),
        ('admin', 'Admin'),
    )

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    discriminator = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    avatar_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, default='offline')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        if self.discriminator:
            return f"{self.username}#{self.discriminator}"
        return self.username
