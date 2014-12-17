from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import  ModelSerializer,Serializer,CharField
from models import Secret,Conversation

class UserSerializer(Serializer):
    UID= CharField(max_length=100)
class ConversationSerializer(ModelSerializer):
    class Meta:
        model =Conversation

class SecretSerializer(ModelSerializer):
    class Meta:
        model =Secret
