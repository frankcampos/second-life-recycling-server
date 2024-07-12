from django.db import models


class Shopping_Cart(models.Model):
    user_id = models.IntegerField()
    item_id = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    total = models.IntegerField(max_digits=10000, decimal_places=2)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    