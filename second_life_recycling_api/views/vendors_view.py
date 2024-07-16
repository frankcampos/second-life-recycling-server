"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from second_life_recycling_api.models import Vendors


class VendorsView(ViewSet):
    """Second Life Recycling Vendors view"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single vendor
    
        Returns:
            Response -- JSON serialized vendor
        """
        vendor = Vendors.objects.filter(pk=pk).first()
    
        if vendor is None:
            return Response({'message': 'Vendor not found.'}, status=status.HTTP_404_NOT_FOUND)
    
        serializer = VendorsSerializer(vendor)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all vendors

        Returns:
            Response -- JSON serialized list of vendors
        """
        try:
            vendor = Vendors.objects.all()
            serializer = VendorsSerializer(vendor, many=True)
            return Response(serializer.data)
        except Vendors.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

class VendorsSerializer(serializers.ModelSerializer):
    """JSON serializer for vendors
    """
    class Meta:
        model = Vendors
        fields = ('vendor_name', 'vendor_address')
