from rest_framework import status
from rest_framework.test import APITestCase
from second_life_recycling_api.models import Recyclable_Items, User, Vendors, Categories
from second_life_recycling_api.views.recyclable_items import RecyclableItemsSerializer
from django.urls import reverse
from django.utils import timezone

class RecyclableItemsTests(APITestCase):
    
    fixtures = ['categories.json', 'recyclable_items.json', 'users.json', 'vendors.json']

    def setUp(self):
        self.recyclable_items = Recyclable_Items.objects.first()
        self.vendor = Vendors.objects.first()
        self.user = User.objects.first()
        self.category = Categories.objects.first()
    
        if self.recyclable_items is None or self.vendor is None or self.user is None or self.category is None:
            self.fail("No recyclable_items, vendors, users, or categories available in fixtures")

        self.url = reverse('recyclable_items-detail', kwargs={'pk': self.recyclable_items.pk})   

    def test_get_single_recyclable_item(self):
        """Get single Recyclable Item test"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check the response data
        response_data = response.json()
        self.assertEqual(response_data['id'], self.recyclable_items.id)
        self.assertEqual(response_data['item_name'], self.recyclable_items.item_name)
        self.assertEqual(response_data['user_id'], self.user.id)

        non_existent_url = reverse('recyclable_items-detail', kwargs={'pk': 999})
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 

    def test_list_all_recyclable_items(self):
        """Test list all Recyclable_Items"""
        url = reverse('recyclable_items-list')
        response = self.client.get(url)
        all_Recyclable_Items = Recyclable_Items.objects.all()
        expected = RecyclableItemsSerializer(all_Recyclable_Items, many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)
    
    def test_create_recyclable_items(self):
        """Create a Recyclable Item test"""
        url = "/recyclable_items"
        recyclable_items_payload = {
            "item_name": "test item",
            "vendor_id": self.vendor.id,
            "vendor_name": self.vendor.vendor_name,
            "price": 20.00,
            "image_url": "www.test.com/image.jpg",
            "user": self.user.id,
            "description": "test description",
            "category_id": self.category.id,
            "created_at": timezone.now(),
            "updated_at": timezone.now()
        }
        response = self.client.post(url, recyclable_items_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_change_recyclable_items(self):
        """Test changing a Recyclable Item"""
        update_data = {
            'item_name': 'Updated Item Name',
            'vendor_id': self.vendor.id,
            'price': 19.99,
            'image_url': 'http://example.com/updated_image.jpg',
            'user': self.user.id,
            'description': 'Updated Description',
            'category_name': self.category.category_name
        }
        response = self.client.put(self.url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_recyclable_item(self):
        """Test delete recyclable item"""
        recyclable_item = Recyclable_Items.objects.first()
    
        url = f'/recyclable_items/{recyclable_item.id}'
        
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
    
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)    