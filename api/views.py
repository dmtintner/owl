from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
import hashlib
from datetime import datetime
from secret_dispenser.serialisers import  UserSerializer
@api_view(['POST'])

def create_auth(request):
    '''
    Serialises data from a request which contoains a UID.
    Generates a new user whose username is that UID and password is a hash of the current time
    '''
    serialized = UserSerializer(data=request.DATA)
    if serialized.is_valid():
        User.objects.create_user(
            "anon@anon.com",
            serialized.init_data['UID'],
            hashlib.sha256(datetime.now()).hexdigest()
        )
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

def InitateConversation(request):
    pass
def RespondToConversation(request):
    pass