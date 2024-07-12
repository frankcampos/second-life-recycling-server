from django.db import models


class Recyclable_Items(models.Model):
    item_name = models.CharField(max_length=100)
    pickup_location = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=100)
    user_id = models.IntegerField()
    description = models.CharField(max_length=100)
    catergory_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    