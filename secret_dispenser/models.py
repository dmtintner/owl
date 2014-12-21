from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class TimeStampModel(models.Model):
    class  Meta:
        abstract =True
    created = models.Field(models.DateTimeField,default=datetime.now(),blank=False,null=False)
    last_update =models.Field(models.DateTimeField,default=datetime.now(),blank=False,null=False)
    def save(self):
        self.date_modified = datetime.now()
        super(TimeStampModel, self).save()
        


class Secret(TimeStampModel):
    AuthoringUser = models.Field(models.ForeignKey(User),null=False,db_index=True)
    Content = models.Field(models.TextField())
    NumberOfReplys = models.Field(models.IntegerField,default=1,null=False,db_index=True)
    ReplysTo = models.ForeignKey('self')
    Conversation = models.ForeignKey(Conversation)
    @staticmethod
    def CreateSecret(AutheringUser,Content,ReplyTo=None):
        S =Secret()
        S.AuthoringUser = AutheringUser
        S.Content =Content
        S.ReplysTo=ReplyTo
        S.save()
        return S

class Conversation(models.Model):
    Initiator =models.Field(models.ForeignKey(User),null=False,db_index=True)
    Replyer = models.Field(models.ForeignKey(User),null=True,db_index=True)
    InitialMessage = models.ForeignKey(Secret,db_index=True,null=False)
    LatestMessage = models.ForeignKey(Secret,db_index=True,null=False)

    @staticmethod
    def InitateConversation(Initiator,InitalText):
        C = Conversation()
        C.Initiator=Initiator
        C.InitialMessage =Secret.CreateSecret(Initiator,InitalText)
        C.LatestMessage=C.InitialMessage
        C.save()
        return C

