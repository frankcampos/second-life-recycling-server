from django.db import models
from .vendors import Vendors
from .categories import Categories
from .user import User

class Recyclable_Items(models.Model):
    item_name = models.CharField(max_length=100)
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE, db_column='vendor_id', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    