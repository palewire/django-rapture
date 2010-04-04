from django.conf.urls.defaults import *

from django.conf import settings

urlpatterns = patterns('',

    url(r'^$', 'archive.views.index', name="rapture-index"),
    
    # Data downloads
    url(r'^download/csv/$', 'data.views.csv', name="rapture-download-csv"),
    url(r'^download/json/$', 'data.views.json', name="rapture-download-json"),
    url(r'^download/xml/$', 'data.views.xml', name="rapture-download-xml"),
    url(r'^download/xls/$', 'data.views.xls', name="rapture-download-xls"),
    
    # Archives
    url(r'^archive/snapshot/list/$', 'archive.views.archive_list', name="rapture-archive-list"),
    url(r'^archive/snapshot/(?P<id>[0-9]+)/$', 'archive.views.archive_detail', name="rapture-archive-detail"),
    url(r'^archive/snapshot/media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}, name="rapture-archive-media"),

)









