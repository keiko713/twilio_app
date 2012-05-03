from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'polls.views.index'),
    url(r'^view/(?P<poll_id>\d+)/$', 'polls.views.view'),
    url(r'^phone_vote/$', 'polls.views.phone_vote'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
