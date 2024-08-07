
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from second_life_recycling_api.models import Categories
from second_life_recycling_api.views import CategoriesSerializer


class CategoriesTests(APITestCase):

  def setUp(self):
    self.category = Categories.objects.create(category_name = "test category")


    self.url = reverse('categories-detail',kwargs={'pk':self.category.pk})
    self.invalid_url = reverse('categories-detail', kwargs={'pk': 9999})
  def test_get_single_category_with_pk(self):
    response = self.client.get(self.url)
    expected_data = CategoriesSerializer(self.category).data

    self.assertEqual(response.data, expected_data)

  def test_get_single_category_without_pk(self):
    response = self.client.get(self.invalid_url)

    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    self.assertEqual(response.data,{'message': 'Category not found.'})
