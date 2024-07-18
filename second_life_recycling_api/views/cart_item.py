from rest_framework import viewsets
from rest_framework import serializers, status
from rest_framework.response import Response
from second_life_recycling_api.models import CartItem, User, RecyclableItem, ShoppingCart

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def create(self, request):
        user = User.objects.get(id=request.data['user'])
        cart = ShoppingCart.objects.get(id=request.data['cart'])
        item = RecyclableItem.objects.get(id=request.data['item'])
        cart_item = CartItem.objects.create(cart=cart, item=item)
        cart_item.save()
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        cart_item = CartItem.objects.get(id=pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        cart_item = CartItem.objects.get(id=pk)
        cart_item.cart = ShoppingCart.objects.get(id=request.data['cart'])
        cart_item.item = RecyclableItem.objects.get(id=request.data['item'])
        cart_item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
