from django.db import models


class Shopping_Cart(models.Model):
    user_id = models.IntegerField()
    item_id = models.IntegerField()
    price = models.DecimalField(default=0, max_digits=17, decimal_places=2)
    status = models.CharField(max_length=50)
    total = models.DecimalField(default=0, max_digits=17, decimal_places=2)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
