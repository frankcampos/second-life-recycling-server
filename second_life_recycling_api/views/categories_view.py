"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from second_life_recycling_api.models import Categories


class CategoriesView(ViewSet):
    """Second Life Recycling Categories view"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single category
    
        Returns:
            Response -- JSON serialized category
        """
        category = Categories.objects.filter(pk=pk).first()
    
        if category is None:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
    
        serializer = CategoriesSerializer(category)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all categories

        Returns:
            Response -- JSON serialized list of categories
        """
        try:
            category = Categories.objects.all()
            serializer = CategoriesSerializer(category, many=True)
            return Response(serializer.data)
        except Categories.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

class CategoriesSerializer(serializers.ModelSerializer):
    """JSON serializer for vendors"""
    class Meta:
        model = Categories
        fields = ('category_name',)
