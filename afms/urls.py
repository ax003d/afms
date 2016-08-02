from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout, password_reset_done, \
    password_reset_confirm, password_reset_complete


admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'afms.views.home', name='home'),
    # url(r'^afms/', include('afms.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^registration/password_reset_done/$', password_reset_done),
    url(r'^registration/password_reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm),
    url(r'^registration/password_reset_complete/$', password_reset_complete),
    url(r'^activity/', include('activity.urls')),
)


urlpatterns += patterns('activity.views',
    url(r'^$', 'profile'),
    url(r'^accounts/profile/$', 'profile'),
    url(r'^registration/password_reset/$', 'password_reset'),
    url(r'^verify/username/$', 'verify_username'),
    url(r'^verify/email/$', 'verify_email'),

    url(r'^preview/markdown/$', 'preview__markdown'),
)
