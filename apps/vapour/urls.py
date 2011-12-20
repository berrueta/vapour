
from django.conf.urls.defaults import patterns, include, url
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from vapour.cup.djng.cup import GET
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r"^favicon.ico",   lambda request: HttpResponseRedirect(settings.MEDIA_URL+"images/favicon.ico")),
    (r"^$",             lambda request: HttpResponsePermanentRedirect("/vapour")),
    (r"^vapour$",       GET)
)

