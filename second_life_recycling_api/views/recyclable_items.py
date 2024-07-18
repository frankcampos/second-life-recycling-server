from rest_framework import viewsets
from rest_framework import serializers, status
from rest_framework.response import Response
from second_life_recycling_api.models import RecyclableItem, User, Company

class RecyclableItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecyclableItem
        fields = '__all__'

class RecyclableItemViewSet(viewsets.ModelViewSet):
    queryset = RecyclableItem.objects.all()
    serializer_class = RecyclableItemSerializer

    def create(self, request):
        user = User.objects.get(id=request.data['user'])
        location = Company.objects.get(id=request.data['location'])
        recyclable_item = RecyclableItem.objects.create(
            item_name=request.data['item_name'],
            price=request.data['price'],
            image_url=request.data['image_url'],
            user=user,
            location=location,
            description=request.data['description'],
            category=request.data['category']
        )
        recyclable_item.save()
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        recyclable_item = RecyclableItem.objects.get(id=pk)
        recyclable_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        recyclable_item = RecyclableItem.objects.get(id=pk)
        user = User.objects.get(id=request.data['user'])
        location = Company.objects.get(id=request.data['location'])
        recyclable_item.item_name = request.data['item_name']
        recyclable_item.price = request.data['price']
        recyclable_item.image_url = request.data['image_url']
        recyclable_item.user = user
        recyclable_item.location = location
        recyclable_item.description = request.data['description']
        recyclable_item.category = request.data['category']
        recyclable_item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        items = RecyclableItem.objects.all()
        serializer = RecyclableItemSerializer(items, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = RecyclableItem.objects.get(id=pk)
        serializer = RecyclableItemSerializer(item)
        return Response(serializer.data)
