from django.db import models
from .user import User
from .company import Company


class RecyclableItem(models.Model):
    item_name = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.CharField(max_length=100)
