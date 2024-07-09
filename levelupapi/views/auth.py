from levelupapi.models import Gamer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def check_user(request):
    '''Checks to see if User has Associated Gamer

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    gamer = Gamer.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if gamer is not None:
        data = {
            'id': gamer.id,
            'uid': gamer.uid,
            'bio': gamer.bio
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)


@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Now save the user info in the levelupapi_gamer table
    gamer = Gamer.objects.create(
        bio=request.data['bio'],
        uid=request.data['uid']
    )

    # Return the gamer info to the client
    data = {
        'id': gamer.id,
        'uid': gamer.uid,
        'bio': gamer.bio
    }
    return Response(data)
