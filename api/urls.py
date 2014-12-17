
from django.conf.urls import patterns, include, url
from views import create_auth
urlpatterns = ('',
                       '^register/$',create_auth
)
