from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'polls.views.index'),
    url(r'^view/(?P<poll_id>\d+)/$', 'polls.views.view'),
    url(r'^web_vote/(?P<poll_id>\d+)/$', 'polls.views.web_vote'),
    url(r'^vote/(?P<choice_id>\d+)/$', 'polls.views.vote'),

    url(r'^sms/$', 'django_twilio.views.sms', {
        'message': 'Thanks for your vote!',
    }),
    url(r'^phone_vote/$', 'polls.views.phone_vote'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
