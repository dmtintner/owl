from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
import hashlib
from datetime import datetime
from secret_dispenser.models import Conversation, Secret
from secret_dispenser.serialisers import  UserUIDSerializer, UserSerialser,ConversationSerializer


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

@api_view(['POST'])
def InitiateConversation(request):
    '''
    Expects an Initiator (the username)
    Expects a MessageBody
    '''
    try:
        Initiator = User.objects.get(username=request.DATA["initator"])
        Conv = Conversation.InitateConversation(Initiator,request.DATA["message_body"])
        serialized = ConversationSerializer(data=Conv)
    except Conversation.DoesNotExist:
        return Response(data={"status":"ERR","reason":"no matching conversation"})
    except Exception,e:
        return Response(data={"status":"ERR","reason":e})
    else:
        if serialized.is_valid():
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def RespondToConversation(request):
    '''

    :param request:
    :param should have converstaion_id,replyer_user_name and reply_text
    :return:
    '''
    data = request.DATA
    try:
        Conv = Conversation.objects.get(pk=data["converstaion_id"])
        Replyer = User.objects.get(username=data["replyer_user_name"])
        SecretReply = Secret.CreateSecret(Replyer,Conv,Conv.LatestMessage)
        Conv.LatestMessage=SecretReply
        SecretReply.save()
        Conv.save()
    except Conversation.DoesNotExist:
        return Response(data={"status":"ERR","reason":"no matching conversation"})
    except User.DoesNotExist:
        return Response(data={"status":"ERR","reason":"no matching user"})
    except Exception,e:
        return Response(data={"status":"ERR","reason":e})