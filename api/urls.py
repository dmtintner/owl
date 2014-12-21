
from django.conf.urls import patterns, include, url
from api.views import InitiateConversation,RespondToConversation
from views import create_auth
urlpatterns =patterns('',
    url('register/', create_auth),
    url('InitiateConversation/', InitiateConversation),
    url('RespondToConversation/', RespondToConversation),
)
