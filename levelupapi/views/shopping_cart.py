"""View module for handling requests about shopping cart"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Shopping_Cart

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
            