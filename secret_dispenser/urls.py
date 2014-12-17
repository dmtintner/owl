from django.conf.urls import patterns, include, url
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView

urlpatterns =patterns('',
    url('^$', TemplateView.as_view(template_name='index.html'),)
)
