from django.db import models
from .user import User

class ShoppingCart(models.Model):

    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def total(self):
        return sum(item.item.price for item in self.cart_items.all())
