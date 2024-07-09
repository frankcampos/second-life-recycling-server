"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game, EventGamer


class EventView(ViewSet):
    """Level up events"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        try:
            event = Event.objects.get(pk=pk)
            serializers = EventSerializer(event)
            return Response(serializers.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to events resource

        Returns:
            Response -- JSON serialized list of events

        """
        uid = request.META['HTTP_AUTHORIZATION']

        gamer = Gamer.objects.get(uid=uid)
        events = Event.objects.all()
        game = request.query_params.get('game', None)
        if game is not None:
            events = events.filter(game_id=game)



        for event in events:
            # Check to see if there is a row in the Event Games table that has the passed in gamer and event
            joined = len(EventGamer.objects.filter(
                gamer=gamer, event=event)) > 0
            if joined:
                event.joined = True
            else:
                event.joined = False


        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized event instance
        """
        organizer = Gamer.objects.get(uid=request.data["userId"])
        game = Game.objects.get(pk=request.data["game"])

        event = Event.objects.create(
            organizer=organizer,
            date=request.data["date"],
            time=request.data["time"],
            game=game,
            description=request.data["description"],
        )

        serializer = EventSerializer(event)

        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        organizer = Gamer.objects.get(uid=request.data["userId"])
        game = Game.objects.get(pk=request.data["game"])

        event = Event.objects.get(pk=pk)
        event.organizer = organizer
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.game = game
        event.description = request.data["description"]
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for a single event

        Returns:
            Response -- 200, 404, or 500 status code
        """

        event = Event.objects.get(pk=pk)
        event.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(uid=request.data["uid"])
        event = Event.objects.get(pk=pk)
        attendee = EventGamer.objects.create(
            gamer=gamer,
            event=event
        )
        self.joined = True
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""

        gamer = Gamer.objects.get(uid=request.data["uid"])
        event = Event.objects.get(pk=pk)
        attendees = EventGamer.objects.filter(gamer=gamer, event=event)
        if attendees:
            for attendee in attendees:

                attendee.delete()
            self.joined = False
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'Gamer not found in event'}, status=status.HTTP_404_NOT_FOUND)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events

    Arguments:
        serializers
    """

    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date',
                  'time', 'organizer', 'joined')
        depth = 2
