
from django.conf.urls.defaults import patterns, include, url
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.views.static import serve
from vapour.cup.djng import cup
from settings import DEBUG, STATIC_URL, STATIC_ROOT

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r"^$",             lambda request: HttpResponsePermanentRedirect("/vapour")),
    (r"^vapour$",       cup.GET),
    (r"^favicon.ico",   lambda request: HttpResponseRedirect(STATIC_URL+"images/favicon.png"))
)

if DEBUG:
    urlpatterns += patterns('',
            (r"^%s(?P<path>.*)$" % STATIC_URL[1:], serve, {"document_root": STATIC_ROOT}),
    )

