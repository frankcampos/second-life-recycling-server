from django.db import models
from .recyclable_items import Recyclable_Items
from .shopping_cart import Shopping_Cart

class CartItem(models.Model):
    cart = models.ForeignKey(Shopping_Cart, on_delete=models.CASCADE, related_name = "cart_items")
    item = models.ForeignKey(Recyclable_Items, on_delete=models.CASCADE, related_name= "cart_items")
