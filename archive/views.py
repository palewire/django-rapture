# Utils
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template

# Models
from rapture.update.models import *
from rapture.data.models import *

def index(request):
    """
    The homepage.
    """
    # Pull the last updated time for timestamps
    last_updated = UpdateLog.objects.last_updated()
    
    # Pull a list of the archived pages that can be reviewed.
    scrape_list = UpdateLog.objects.complete().order_by("-end_date")
    
    # Pull a list of all the editions we have published
    edition_list = Edition.objects.all()
    
    return direct_to_template(request, 'rapture/archive/index.html', {
        'last_updated': last_updated,
        'scrape_list': scrape_list,
        'edition_list': edition_list
    })

def archive_list(request):
    scrape_list = UpdateLog.objects.complete().order_by("-end_date")
    return direct_to_template(request, 'rapture/archive/archive_list.html', {
        'scrape_list': scrape_list
    })

def archive_detail(request, id):
    update = get_object_or_404(UpdateLog, id=id)
    return direct_to_template(request, 'rapture/archive/archive_detail.html', {
        'update_log': update,
    })
