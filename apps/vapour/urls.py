
from django.conf.urls import patterns, include, url, handler404
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.views.static import serve
from vapour.cup.webclient import cup
from settings import DEBUG, STATIC_URL, STATIC_ROOT

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r"^$",             lambda request: HttpResponsePermanentRedirect("/vapour")),
    (r"^vapour$",       cup.GET),
    (r"^vapour/$",      lambda request: HttpResponsePermanentRedirect("/vapour")),
    #(r"^favicon.ico",   lambda request: HttpResponseRedirect(MEDIA_URL+"images/favicon.png"))
    (r"^%s(.*)$" % STATIC_URL[1:], serve, {"document_root": STATIC_ROOT})
)
