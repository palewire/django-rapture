# Utils
import os
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from BeautifulSoup import BeautifulSoup

# Models
from update.models import *
from data.models import *

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
	
	return direct_to_template(request, 'index.html', {
		'last_updated': last_updated,
		'scrape_list': scrape_list,
		'edition_list': edition_list
	})


def archive_detail(request, id):
	update = get_object_or_404(UpdateLog, id=id)
	return direct_to_template(request, 'archive_detail.html', {
		'update_log': update,
	})