from django.conf.urls import patterns, include, url
from django.shortcuts import render_to_response

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from lastFm import views
from sevenDigital import views
admin.autodiscover()

import lastFm
import sevenDigital

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'F:/MusicPush/media'}),

    (r'^$','mysite.views.index'),
    (r'^home$','mysite.views.index'),
    (r'^logout$','mysite.views.logout'),
    (r'^verifyUser$','mysite.views.verifyUser'),
    (r'^register$','mysite.views.register'),
    (r'^createUser$','mysite.views.createUser'),
    (r'^favList$','mysite.views.favList'),
    (r'^hotList$','mysite.views.hotList'),

    (r'^getTrack$',lastFm.views.getTrack),
    (r'^getHotList$',lastFm.views.getHotList),
    (r'^getFavList$',lastFm.views.getFavList),
    (r'^searchTrack$',lastFm.views.searchTrack),
    (r'^getRecommendation$',lastFm.views.getRecommendation),

    (r'^love$',lastFm.views.love),
    (r'^hate$',lastFm.views.hate),
    (r'^cycle$',lastFm.views.cycle),
    (r'^skip$',lastFm.views.skip),
    (r'^cancelLove$',lastFm.views.cancelLove),
)
