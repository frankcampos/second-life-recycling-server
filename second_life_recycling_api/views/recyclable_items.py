from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import HttpResponseServerError
from django.utils import timezone

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
        fields = ('id', 'item_name', 'vendor_id', 'price', 'image_url', 'user_id', 'description', 'category_id', 'created_at', 'updated_at')
        depth = 1
        
class RecyclableItemsViewSet(viewsets.ModelViewSet):
    """Level up recyclable items types view"""
    
    queryset = Recyclable_Items.objects.all()
    serializer_class = RecyclableItemsSerializer
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single recyclable item type

        Returns:
            Response -- JSON serialized recyclable item type
        """
        try:
            recyclable_item = self.get_object()
            serializer = RecyclableItemsSerializer(recyclable_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
        try:
            print(f"Incoming data: {request.data}")
            
            user_id = request.data.get("user_id", None)
            vendor_id = request.data.get("vendor_id")
            category_id = request.data.get("category_id")
    
            if not vendor_id:
                print("Vendor ID is missing.")
                return Response({'message': 'Vendor ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
            if not category_id:
                print("Category ID is missing.")
                return Response({'message': 'Category ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
            try:
                vendor = Vendors.objects.get(pk=vendor_id)
                print(f"Vendor found: {vendor}")
            except Vendors.DoesNotExist:
                print("Vendor not found.")
                return Response({'message': 'Vendor not found.'}, status=status.HTTP_404_NOT_FOUND)
    
            try:
                category = Categories.objects.get(pk=category_id)
                print(f"Category found: {category}")
            except Categories.DoesNotExist:
                print("Category not found.")
                return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
    
            user, created = User.objects.get_or_create(id=user_id)
            print(f"User found or created: {user}")
    
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
            print(f"Recyclable item created: {recyclable_item}")
    
            serializer = RecyclableItemsSerializer(recyclable_item)
            print(f"Serialized data: {serializer.data}")
    
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def update(self, request, *args, **kwargs):
        print(f"Incoming data: {request.data}")
        try:
            instance = self.get_object()
            vendor_id = request.data.get("vendor_id")
            category_name = request.data.get("category_name")
    
            if not vendor_id:
                return Response({'message': 'Vendor ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
            if not category_name:
                return Response({'message': 'Category name is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
            try:
                vendor = Vendors.objects.get(pk=vendor_id)
            except Vendors.DoesNotExist:
                return Response({'message': 'Vendor not found.'}, status=status.HTTP_404_NOT_FOUND)
    
            try:
                category = Categories.objects.get(category_name=category_name)
            except Categories.DoesNotExist:
                return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
    
            # Update the instance with the new data
            instance.vendor = vendor
            instance.item_name = request.data.get("item_name", instance.item_name)
            instance.price = request.data.get("price", instance.price)
            instance.image_url = request.data.get("image_url", instance.image_url)
            instance.description = request.data.get("description", instance.description)
            instance.category = category
            instance.updated_at = timezone.now()
            instance.save()
    
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk):
        try:
            recyclable_item = Recyclable_Items.objects.get(pk=pk)
            recyclable_item.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Recyclable_Items.DoesNotExist:
            return Response({'message': 'Recyclable Item not found.'}, status=status.HTTP_404_NOT_FOUND)
