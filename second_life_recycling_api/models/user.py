from django.db import models
from django.utils import timezone

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    uid = models.CharField(max_length=50)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True)
