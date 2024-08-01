from django.http import HttpResponseServerError
from django.utils import timezone
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db import models
from datetime import datetime
from second_life_recycling_api.models import Recyclable_Items, User, Vendors, Categories
from second_life_recycling_api.views.auth import check_user

class RecyclableItemsSerializer(serializers.ModelSerializer):
    """JSON serializer for Recyclable Items types"""
    class Meta:
        model = Recyclable_Items
        fields = ('id', 'item_name','vendor', 'price', 'image_url', 'user_id', 'description', "category", 'created_at', 'updated_at')
        depth = 1

class RecyclableItems(ViewSet):
    """Level up recyclable items types view"""
    queryset = Recyclable_Items.objects.all()
    serializer_class = RecyclableItemsSerializer
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
        vendor_id = request.query_params.get("type", None)
        if vendor_id is not None:
            games = games.filter(vendor_id=vendor_id)
        category_id = request.query_params.get("type", None)
        if category_id is not None:
            games = games.filter(vendor_id=vendor_id)
        serializer = RecyclableItemsSerializer(recyclable_items, many=True)
        return Response(serializer.data)

    def create(self, request):
        user_id = request.data.get("user_id", None)
        vendor = Vendors.objects.get(pk=request.data["vendor_id"])
        category = Categories.objects.get(pk=request.data["category"])
        user, created = User.objects.get_or_create(id=user_id)
        recyclable_item = Recyclable_Items.objects.create(
            item_name=request.data["item_name"],
            vendor=vendor,
            price=request.data["price"],
            image_url=request.data["image_url"],
            user=user,
            description=request.data["description"],
            category=category,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        serializer = RecyclableItemsSerializer(recyclable_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED) 

    def update(self, request, pk):
        try:
            recyclable_item = Recyclable_Items.objects.get(pk=pk)
            recyclable_item.item_name = request.data["item_name"]
            vendors = Vendors.objects.get(pk=request.data.get("vendor_id"))
            recyclable_item.vendor = vendors
            recyclable_item.price = request.data["price"]
            recyclable_item.image_url = request.data["image_url"]
            user_id = User.objects.get(pk=request.data.get("user_id"))
            recyclable_item.user = user_id
            recyclable_item.description = request.data["description"]
            categories = Categories.objects.get(pk=request.data["category"])
            recyclable_item.category = categories
            recyclable_item.created_at = request.data["created_at"]
            recyclable_item.updated_at = request.data["updated_at"]
            recyclable_item.save()

            serializer = RecyclableItemsSerializer(recyclable_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Recyclable_Items.DoesNotExist:
            return Response({'message': 'Recyclable Item not found.'}, status=status.HTTP_404_NOT_FOUND)



    def destroy(self, request, pk):
        try:
            recyclable_item = Recyclable_Items.objects.get(pk=pk)
            recyclable_item.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Recyclable_Items.DoesNotExist:
            return Response({'message': 'Recyclable Item not found.'}, status=status.HTTP_404_NOT_FOUND)
