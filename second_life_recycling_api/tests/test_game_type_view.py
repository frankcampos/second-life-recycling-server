from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from levelupapi.models import GameType, Gamer
from levelupapi.views.game_type import GameTypeSerializer


# create the test function for game_type and pass the APITestCase
class GameTypeTest(APITestCase):

    def setUp(self):
        self.user = Gamer.objects.first()
        self.game_type = GameType.objects.create(label='chess')

    def test_get_gametype(self):
        game_type = GameType.objects.first()
        print('this is the gametype', game_type)
        url = f'/gametypes/{game_type.id}'
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_list_gametype(self):
        url = '/gametypes'
        response = self.client.get(url)
        game_types = GameType.objects.all()
        expected = GameTypeSerializer(game_types, many=True).data
        self.assertEqual(expected, response.data)
