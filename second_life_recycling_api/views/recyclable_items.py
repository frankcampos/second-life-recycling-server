from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from datetime import datetime
from second_life_recycling_api.models import Recyclable_Items, User

class RecyclableItemsSerializer(serializers.ModelSerializer):
    """JSON serializer for Recyclable Items types"""
    class Meta:
        model = Recyclable_Items
        fields = ('id', 'item_name','vendor', 'price', 'image_url', 'user_id', 'description', "category", 'created_at', 'updated_at')

class RecyclableItems(ViewSet):
    """Level up recyclable items types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single recyclable item type

        Returns:
            Response -- JSON serialized recyclable item type
        """
        try:
            recyclable_item = Recyclable_Items.objects.get(pk=pk)
            serializer = RecyclableItemsSerializer(recyclable_item)
            return Response(serializer.data)
        except Recyclable_Items.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all recyclable items types

        Returns:
            Response -- JSON serialized list of recyclable items types
        """
        recyclable_items = Recyclable_Items.objects.all()
        serializer = RecyclableItemsSerializer(recyclable_items, many=True)
        return Response(serializer.data)
        
    def create(self, request):
        uid = request.data["userId"]
        user, created = User.objects.get_or_create(uid=uid)
       
        recyclable_item = Recyclable_Items.objects.create(
            item_name=request.data["item_name"],
            vendor=request.data["vendor"],
            price=request.data["price"],
            image_url=request.data["image_url"],
            category=request.data["category"],
            created_at = datetime.now(),
            updated_at = datetime.now()
        )
        serializer = RecyclableItemsSerializer(recyclable_item)
        return Response(serializer.data)
     
    def update(self, request, pk):
        recyclable_item = Recyclable_Items.objects.get(pk=pk)
        recyclable_item.item_name = request.data["item_name"]
        recyclable_item.vendor = request.data["vendor"]
        recyclable_item.price = request.data["price"]
        recyclable_item.image_url = request.data["image_url"]
        recyclable_item.user_id = request.data["user_id"]
        recyclable_item.description = request.data["description"]
        recyclable_item.category = request.data["category"]
        recyclable_item.created_at = request.data["created_at"]
        recyclable_item.updated_at = request.data["updated_at"]
        recyclable_item.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    queryset = Recyclable_Items.objects.all()
    serializer_class = RecyclableItemsSerializer
    
    def destroy(self, request, pk):
        try:
            recyclable_item = Recyclable_Items.objects.get(pk=pk)
            recyclable_item.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Recyclable_Items.DoesNotExist:
            return Response({'message': 'Recyclable_Item not found.'}, status=status.HTTP_404_NOT_FOUND)