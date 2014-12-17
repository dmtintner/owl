from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import  ModelSerializer,Serializer,CharField
from models import Secret,Conversation
from django.contrib.auth.models import User

class UserUIDSerializer(Serializer):
    UID= CharField(max_length=100)
class UserSerialser(ModelSerializer):
    class Meta:
        model = User
class ConversationSerializer(ModelSerializer):
    class Meta:
        model =Conversation

class SecretSerializer(ModelSerializer):
    class Meta:
        model =Secret
