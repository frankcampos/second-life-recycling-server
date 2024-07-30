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
        
    def test_create_recyclable_items(self):
        """Create Recyclable Items test"""
        url = "/recyclable_items"
        recyclable_items_payload = {
            "item_name": "test item",
            "vendor_id": Vendors.objects.first().id,  # Changed key to match expected 'vendor_id'
            "price": 20.00,
            "image_url": "www.test.com/image.jpg",
            "user": 1,
            "description": "test description",
            "category": Categories.objects.first().id,
            "created_at": timezone.now(),  # Use timezone-aware datetime
            "updated_at": timezone.now()   # Use timezone-aware datetime
        }
        response = self.client.post(url, recyclable_items_payload, format='json')
        print(response.content)  # Print response content for debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_recyclable_items(self):
        """Get Recyclable Item test"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test for a non-existent item
        non_existent_url = reverse('recyclable_items-detail', kwargs={'pk': 999})
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 

    def test_list_recyclable_items(self):
        """Test list Recyclable_Items"""
        url = '/recyclable_items'
        response = self.client.get(url)
        all_Recyclable_Items = Recyclable_Items.objects.all()
        expected = RecyclableItemsSerializer(all_Recyclable_Items, many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)