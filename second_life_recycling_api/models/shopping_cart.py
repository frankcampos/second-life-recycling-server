from django.db import models
from .user import User
from .recyclable_items import Recyclable_Items
class Shopping_Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    total = models.DecimalField(default=0, max_digits=17, decimal_places=2)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    @property
    def total(self):
        return sum(item.item.price for item in self.cart_items.all())
