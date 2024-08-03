"""View module for handling requests about shopping cart"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from second_life_recycling_api.models import User, Shopping_Cart, Recyclable_Items, CartItem
from rest_framework.decorators import action
from .recyclable_items import RecyclableItemsSerializer


class CartSerializer(serializers.ModelSerializer):
    """JSON serializer for shopping carts"""
    class Meta:
        model = Shopping_Cart
        fields = ('user', 'status', 'total', 'created_at', 'updated_at')
        depth = 1


class CartItemSerializer(serializers.ModelSerializer):
    """JSON serializer for cart items"""

    class Meta:
        model = CartItem
        fields = '__all__'
        depth = 1


class ShoppingCartView(ViewSet):
    """Shopping cart view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type"""
        try:
            shopping_cart = Shopping_Cart.objects.get(pk=pk)
            serializer = CartSerializer(shopping_cart)
            return Response(serializer.data)
        except Shopping_Cart.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types"""
        shopping_carts = Shopping_Cart.objects.all()
        serializer = CartSerializer(shopping_carts, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations"""
        user_id = User.objects.get(uid=request.data["user_id"])
        item_id = Recyclable_Items.objects.get(pk=request.data["item_id"])

        cart = Shopping_Cart.objects.create(
            user_id=user_id,
            item_id=item_id,
            status=request.data["status"],
            total=request.data["total"],
            created_at=request.data["created_at"],
            updated_at=request.data["updated_at"],

        )
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for shopping cart"""

        cart = Shopping_Cart.objects.get(pk=pk)
        cart.status = request.data["status"],
        cart.total = request.data["total"],
        cart.created_at = request.data["created_at"],
        cart.updated_at = request.data["updated_at"]

        item_id = Recyclable_Items.objects.get(pk=request.data["item_id"])
        cart.item_id = item_id
        cart.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for shopping cart"""
        cart = Shopping_Cart.objects.get(pk=pk)
        cart.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, url_path="add_to_cart")
    def add_to_cart(self, request, pk=None):
        """post req for user to add item to cart"""

        user = User.objects.get(id=request.data["userId"])
        item = Recyclable_Items.objects.get(id=request.data["itemId"])
        try:
            cart = Shopping_Cart.objects.get(user=user)
        except:
            cart = Shopping_Cart.objects.create(
                user=user,
                status=True,
            )
        cart.save()
        CartItem.objects.create(
            cart=cart,
            item=Recyclable_Items.objects.get(id=request.data["itemId"])
        )
        serializer = CartSerializer(cart)
        item_serializer = RecyclableItemsSerializer(item)
        return Response({'cart': serializer.data, 'item': item_serializer.data})

    @action(methods=['post'], detail=False, url_path="remove_from_cart")
    def remove_from_cart(self, request, pk=None):
        """post req for user to remove an item from the cart"""
        try:
            shopping_cart_id = request.data.get('shopping_cart_id')
            item_id = request.data.get('item_id')
            cart = Shopping_Cart.objects.get(id=shopping_cart_id)
            cart_item = CartItem.objects.filter(cart=cart, item_id=item_id)
            cart_item.delete()
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False)
    def display_item(self, request, pk=None):
        """post request to display items in shopping cart"""
        shopping_cart_id = request.data.get('shopping_cart_id')
        cart = Shopping_Cart.objects.get(id=shopping_cart_id)
        item = CartItem.objects.filter(cart=cart)
        item_serializer = CartItemSerializer(item, many=True)

        response_data = {
            'cart_items': item_serializer.data,
            'total': cart.total
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path="checkout")
    # Need to create a new cart
    def checkout(self, request, pk=None):
      shopping_cart_id = request.data.get('shopping_cart_id')
      cart = Shopping_Cart.objects.get(id=shopping_cart_id)
      cart.status = False
      cart.save()
      return Response({'message': 'Thank you for your order.'}, status=status.HTTP_200_OK)
