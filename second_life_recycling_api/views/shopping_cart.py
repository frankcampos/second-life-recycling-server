"""View module for handling requests about shopping cart"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from models import Shopping_Cart, User, Recyclable_Items

class CartSerializer(serializers.ModelSerializer):
  """JSON serializer for shopping carts"""
  class Meta:
    model = Shopping_Cart
    fields = ('user_id', 'item_id', 'price', 'status', 'total', 'created_at', 'updated_at')

class ShoppingCartView(ViewSet):
  """Shopping cart view"""
  

  def retrieve(self, request, pk):
    """Handle GET requests for single game type"""
    shopping_cart = Shopping_Cart.objects.get(pk=pk)
    serializer = CartSerializer(shopping_cart)
    return Response(serializer.data)


  def list(self, request):
    """Handle GET requests to get all game types"""
    shopping_carts = Shopping_Cart.objects.all()
    serializer = CartSerializer(shopping_carts, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    """Handle POST operations"""
    user = User.objects.get(uid=request.data["user_id"])
    item = Recyclable_Items.objects.get(pk=request.data["item_id"])

    cart = Shopping_Cart.objects.create(
      user_id=user,
      item_id=item,
      price=request.data["price"],
      status=request.data["status"],
      total=request.data["total"],
      created_at=request.data["created_at"],
      updated_at=request.data["updated_at"],
            
    )
    serializer = CartSerializer(cart)
    return Response(serializer.data)
