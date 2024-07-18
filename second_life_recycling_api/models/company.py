from django.db import models
from .user import User


class Company(models.Model):
    business_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    location = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
