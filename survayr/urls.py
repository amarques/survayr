from django.conf.urls import patterns, include, url

from django.contrib import admin

from polls.views import IndexView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^', IndexView.as_view()),
)