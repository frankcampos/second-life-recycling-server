from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from levelupapi.models import Event, Gamer
from levelupapi.views.event import EventSerializer


class EventTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['gamers', 'game_types', 'games', 'events']

    def setUp(self):
        # Grab the first Gamer object from the database

        self.organizer = Gamer.objects.first()


    def test_create_event(self):
        """Create event test"""
        url = "/events"

        event = {
            "game": 1,
            "description": "This is a test event",
            "date": "2021-08-18",
            "time": "2021-08-18T14:00:00Z",
            "location": "Nashville",
            "userId": self.organizer.uid
        }

        response = self.client.post(url, event, format='json')

        new_event = Event.objects.last()

        expected = EventSerializer(new_event)

        self.assertEqual(expected.data, response.data)

    def test_get_event(self):
        """Get Event Test
        """
        event = Event.objects.first()

        url = f'/events/{event.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_list_event(self):
        """List Event Test
        """
        url = "/events"

        response = self.client.get(url, HTTP_AUTHORIZATION = self.organizer.uid)
        all_events = Event.objects.all()
        expected = EventSerializer(all_events, many=True).data
        for event in expected:
            event['joined'] = False

          # Temporarily print both for comparison
        print("Expected:", expected)
        print("Actual:", response.data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected, response.data, "Response data does not match expected data")

    def test_update_event(self):
        """Update Event Test
        """
        event = Event.objects.first()

        url = f'/events/{event.id}'

        new_event = {
            "game": 1,
            "description": "This is a test event",
            "date": "2021-08-18",
            "time": "2021-08-18T14:00:00Z",
            "location": "Nashville",
            "userId": self.organizer.uid
        }

        response = self.client.put(url, new_event, format='json')

        self.assertAlmostEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        event.refresh_from_db()

        self.assertEqual(new_event['description'], event.description)
def test_delete_event(self):
        """Delete Event Test
        """
        event = Event.objects.first()

        url = f'/events/{event.id}'

        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Event.objects.filter(id=event.id).exists())
