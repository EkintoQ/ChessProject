from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    total_games = models.IntegerField(blank=True, default=0)
    friends = models.ManyToManyField("self", symmetrical=False)


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(
        CustomUser, related_name="sent_requests", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        CustomUser, related_name="received_requests", on_delete=models.CASCADE
    )
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
