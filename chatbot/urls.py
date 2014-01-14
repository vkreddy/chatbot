from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.conf import settings
from bot.views import *

urlpatterns = patterns('',
    url(r'^$', 'bot.views.home', name='home'),
    # Examples:
    # url(r'^$', 'chatbot.views.home', name='home'),
    # url(r'^chatbot/', include('chatbot.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
