
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from second_life_recycling_api.models import Categories
from second_life_recycling_api.views import CategoriesSerializer


class CategoriesTests(APITestCase):

    def setUp(self):
        self.category = Categories.objects.create(
            category_name="test category")

        self.categories = Categories.objects.all()
        self.url = reverse('categories-detail',
                           kwargs={'pk': self.category.pk})
        self.invalid_url = reverse('categories-detail', kwargs={'pk': 9999})
        self.list_url = reverse('categories-list')

    def test_get_single_category_with_pk(self):
        response = self.client.get(self.url)
        expected_data = CategoriesSerializer(self.category).data

        self.assertEqual(response.data, expected_data)

    def test_get_single_category_without_pk(self):
        response = self.client.get(self.invalid_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'message': 'Category not found.'})

    def test_get_list_categories(self):
        response = self.client.get(self.list_url)
        expected_data = CategoriesSerializer(self.categories, many=True).data

        self.assertEqual(response.data, expected_data)

    def test_get_list_categories_empty(self):
        Categories.objects.all().delete()

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'message': 'Category not found.'})

    def test_create_category(self):
        url = reverse('categories-list')
        category_payload = {
            "category_name": "new category"

        }

        response = self.client.post(url, category_payload, format='json')
        last_category = Categories.objects.last()
        serializer_category = CategoriesSerializer(last_category).data
        self.assertEqual(response.data, serializer_category)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_category(self):

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, 'THE CATEGORY WAS ERASE')

    def test_delete_category_no_pk(self):

        response = self.client.delete(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'message': 'Categories matching query does not exist.'})
