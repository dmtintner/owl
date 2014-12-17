from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class TimeStampModel(models.Model):
    class  Meta:
        abstract =True
    created = models.Field(models.DateTimeField,auto_now_add=True,blank=False,null=False)
    last_update =models.Field(models.DateTimeField,auto_now_add=True,blank=False,null=False)
    def save(self):
        self.date_modified = datetime.now()
        super(TimeStampModel, self).save()
        
class SecretReader(models.Model):
    DateRead = models.Field(models.DateTimeField,auto_now_add=True,blank=False,db_index=True)
    Secret = models.ForeignKey(Secret,db_index=True,null=False)
    Reader = models.ForeignKey(User,null=False)


class Secret(TimeStampModel):
    AuthoringUser = models.Field(models.ForeignKey(User),null=False,db_index=True)
    Content = models.Field(models.TextField())
    NumberOfReplys = models.Field(models.IntegerField,default=1,null=False,index=True)

class SecretReply(TimeStampModel):
    Secret = models.ForeignKey(Secret,db_index=True,null=False)
    Replyer =models.ForeignKey(SecretReader)


