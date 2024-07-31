from rest_framework import status
from rest_framework.test import APITestCase
from second_life_recycling_api.models import Recyclable_Items, User, Vendors, Categories
from second_life_recycling_api.views.recyclable_items import RecyclableItemsSerializer
from django.urls import reverse
from django.utils import timezone

class RecyclableItemsTests(APITestCase):
    fixtures = ['categories.json', 'recyclable_items.json', 'users.json', 'vendors.json']
  
    def setUp(self):
        # Set up initial data
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.vendor = Vendors.objects.create(name='Test Vendor')
        self.category = Category.objects.create(name='Lighting')
        self.item = Recyclable_Items.objects.create(
            item_name='Chandelier',
            vendor=self.vendor,
            price=30.00,
            image_url='www.test.com/image.jpg',
            user=self.user,
            description='test description',
            category=self.category,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        
        # Print detailed information
        print(f"SetUp - first_name: {self.user.first_name}, email: {self.user.email}, id: {self.user.id}")
        print(f"SetUp - Vendor: id: {self.vendor.id}")
        print(f"SetUp - Category: name: {self.category.category_name}, id: {self.category.id}")
        print(f"SetUp - Recyclable Item: item_name: {self.recyclable_items.item_name}, price: {self.recyclable_items.price}, id: {self.recyclable_items.id}")

        if self.recyclable_items is None or self.vendor is None or self.user is None or self.category is None:
            self.fail("No recyclable_items, vendors, users, or categories available in fixtures")

        self.url = f'/recyclable_items/{self.recyclable_items.id}/'
        
    def test_get_single_recyclable_items(self):
        """Get single Recyclable Item test"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        non_existent_url = reverse('recyclable_items-detail', kwargs={'pk': 999})
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 

    def test_list_all_recyclable_items(self):
        """Test list all Recyclable_Items"""
        url = '/recyclable_items'
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
            "category": Categories.objects.first().id,
            "created_at": timezone.now(), 
            "updated_at": timezone.now()  
        }
        response = self.client.post(url, recyclable_items_payload, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
def test_change_recyclable_items(self):
    """test update recyclable items"""
    self.client.force_authenticate(user=self.user)

    # Retrieve vendor again to ensure it's available
    vendor = Vendors.objects.first()

    # Print vendor information
    print(f"Test - Vendor: id={vendor.id}")

    updated_recyclable_items_payload = {
        "item_name": "Updated test item",
        "vendor": vendor.id,
        "price": 20.00,
        "image_url": "www.test.com/image.jpg",
        "user": self.user.id,
        "description": "test description",
        "category": self.category.id,
        "created_at": timezone.now(),
        "updated_at": timezone.now()
    }

    # Print URL and payload
    print(f"Test - URL: {self.url}")
    print(f"Test - Payload: {updated_recyclable_items_payload}")

    response = self.client.put(self.url, updated_recyclable_items_payload, format='json')

    # Print response status code and data
    print(f"Test - Response status code: {response.status_code}")
    if response.status_code != status.HTTP_200_OK:
        print(f"Test - Response content: {response.content}")

    # Assert that the response status code is HTTP 200 OK
    self.assertEqual(response.status_code, status.HTTP_200_OK)