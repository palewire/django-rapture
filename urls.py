from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from django.conf import settings


urlpatterns = patterns('',

	(r'^admin/(.*)', admin.site.root),
	url(r'^$', 'archive.views.index', name="rapture-index"),
	url(r'^archive/snapshot/(?P<id>[0-9]+)/$', 
		'archive.views.archive_detail', name="rapture-archive-detail"),
	url(r'^archive/snapshot/media/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}, name="rapture-archive-media"),


)
	








