from django.db import models
from .shoppingCart import ShoppingCart
from .recyclableItems import RecyclableItem

class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(RecyclableItem, on_delete=models.CASCADE, related_name='cart_items')
