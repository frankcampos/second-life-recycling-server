from rest_framework import status
from rest_framework.test import APITestCase
from second_life_recycling_api.models import Recyclable_Items, User, Vendors, Categories
from second_life_recycling_api.views.recyclable_items import RecyclableItemsSerializer
from django.urls import reverse
from django.utils import timezone

class RecyclableItemsTests(APITestCase):
    
    fixtures = ['categories.json', 'recyclable_items.json', 'users.json', 'vendors.json']

    def setUp(self):
        # print("Setting up test data...")

        self.recyclable_items = Recyclable_Items.objects.first()
        # print(f"Recyclable Item: {self.recyclable_items}")

        self.vendor = Vendors.objects.first()
        # print(f"Vendor: {self.vendor}")

        self.user = User.objects.first()
        # print(f"User: {self.user}")

        self.category = Categories.objects.first()
        # print(f"Category: {self.category}")

        if self.recyclable_items is None or self.vendor is None or self.user is None or self.category is None:
            self.fail("No recyclable_items, vendors, users, or categories available in fixtures")

        self.url = reverse('recyclable_items-detail', kwargs={'pk': self.recyclable_items.pk})
        # print(f"URL: {self.url}")

    def test_get_single_recyclable_item(self):
        """Get single Recyclable Item test"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check the response data
        response_data = response.json()
        self.assertEqual(response_data['id'], self.recyclable_items.id)
        self.assertEqual(response_data['item_name'], self.recyclable_items.item_name)
        self.assertEqual(response_data['user_id'], self.user.id)  # Adjusted to check for user dictionary

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
            "vendor_id": Vendors.objects.first().id,
            "price": 20.00,
            "image_url": "www.test.com/image.jpg",
            "user": 1,
            "description": "test description",
            "category_name": Categories.objects.first().category_name,
            "created_at": timezone.now(), 
            "updated_at": timezone.now()  
        }
        response = self.client.post(self.url, recyclable_items_payload, format='json')
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_change_recyclable_items(self):
        """Test changing a Recyclable Item"""
        update_data = {
            'item_name': 'Updated Item Name',
            'vendor_id': self.vendor.id,
            'price': 19.99,
            'image_url': 'http://example.com/updated_image.jpg',
            'user': self.user.id,  # Corrected field name
            'description': 'Updated Description',
            'category_name': self.category.category_name
        }
        print(f"Update data: {update_data}")
        response = self.client.put(self.url, update_data, format='json')
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)