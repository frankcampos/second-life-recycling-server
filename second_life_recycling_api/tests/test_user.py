from rest_framework import status
from rest_framework.test import APITestCase
from second_life_recycling_api.models import User

# create the class UserTest
class UserTest(APITestCase):
  def setUp(self):
    self.user = User.objects.create(
            first_name="test",
            last_name="test last name",
            photo="urlphoto",
            email="my@email",
            uid="12ksjh2mrm342",
            admin=False
        )

  def test_register_user(self):
    url = "/register"

    user = {
      "first_name": "test",
      "last_name": "test last name",
      "photo": "urlphoto",
      "email": "my@email",
      "uid": "unodos"
    }

    response = self.client.post(url,user, format ='json')

    new_user = User.objects.last()

    self.assertEqual(response.status_code, status.HTTP_200_OK)


  def test_check_user_valid_uid(self):
      url = "/checkuser"

      # self.client check the firs object of my table user
      response = self.client.post(url, {'uid': '12ksjh2mrm342'}, format='json')
      print(response.data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.data['first_name'], self.user.first_name)
      self.assertEqual(response.data['last_name'], self.user.last_name)
      self.assertEqual(response.data['email'], self.user.email)
      self.assertEqual(response.data['uid'], self.user.uid)
      self.assertEqual(response.data['admin'], self.user.admin)

  def test_check_user_invalid_uid(self):
      url = "/checkuser"
      response = self.client.post(url, {'uid': 'invaliduid'}, format='json')
      self.assertFalse(response.data['valid'])
