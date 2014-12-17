from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
import hashlib
from datetime import datetime
from secret_dispenser.serialisers import  UserUIDSerializer, UserSerialser


@api_view(['POST'])

def create_auth(request):
    '''
    Serialises data from a request which contoains a UID.
    Generates a new user whose username is that UID and password is a hash of the current time
    '''
    serialized = UserUIDSerializer(data=request.DATA)
    if serialized.is_valid():
        try:
            U =User.objects.create_user(

                hashlib.sha256(str(datetime.now())).hexdigest(),
                "anon@anon.com",
                hashlib.sha256(str(datetime.now())).hexdigest()
            )
        except Exception, e:
            print e
        serializer = UserSerialser(U)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

def InitateConversation(request):
    pass
def RespondToConversation(request):
    pass