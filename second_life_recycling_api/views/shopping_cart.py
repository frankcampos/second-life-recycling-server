"""View module for handling requests about shopping cart"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from second_life_recycling_api.models import User, CartItem, ShoppingCart

class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        depth = 1

class ShoppingCartView(ViewSet):
    def list(self, request):
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        cart = ShoppingCart.objects.get(user=user)
        serializer = ShoppingCartSerializer(cart)
        return Response(serializer.data)

    def create(self, request):
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        cart = ShoppingCart.objects.create(user=user)
        cart.save()
        serializer = ShoppingCartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        cart = ShoppingCart.objects.get(user=user)
        cart.total = request.data['total']
        cart.save()
        serializer = ShoppingCartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            user_id = request.data.get('user_id')
            user = User.objects.get(id=user_id)
            cart = ShoppingCart.objects.get(user=user)
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ShoppingCart.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def add_item(self, request, pk=None):
      user_id = request.data.get('user_id')
      user = User.objects.get(id=user_id)

      # Check if the cart exists
      try:
          cart = ShoppingCart.objects.get(user=user)
      except ShoppingCart.DoesNotExist:
          # Create a new cart if it doesn't exist
          cart = ShoppingCart.objects.create(user=user, total=0.00)
          cart.save()

      # Add the item to the cart
      cart_item = CartItem.objects.create(
          cart=cart,
          item_id=request.data['item_id']
      )
      cart_item.save()

      # Serialize the cart and return the response
      serializer = ShoppingCartSerializer(cart)
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        try:
            shopping_cart_id = request.data.get('shopping_cart_id')
            item_id = request.data.get('item_id')
            cart = ShoppingCart.objects.get(id=shopping_cart_id)
            cart_item = CartItem.objects.get(cart=cart, item_id=item_id)
            cart_item.delete()
            serializer = ShoppingCartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def get_cart_items(self, request):
        shopping_cart_id = request.data.get('shopping_cart_id')
        cart = ShoppingCart.objects.get(id=shopping_cart_id)
        cart_items = CartItem.objects.filter(cart=cart).all()
        serializer = CartItemSerializer(cart_items, many=True)
        response_data = {
        'cart_items': serializer.data,
        'total': cart.total
    }
        return Response(response_data)

    # def get_cart_total(self, request):
    #     user_id = request.data.get('user_id')
    #     user = User.objects.get(id=user_id)
    #     cart = ShoppingCart.objects.get(user=user)
    #     total = cart.total
    #     return Response({'total': total})
