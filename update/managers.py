# Models
from django.contrib.gis.db import models
from update.models import Update


class LiveUpdateManager(models.GeoManager):
	"""
	Returns the latest live crime stats update.
	
	Example usage:
		
		>>> Update.live.all()
		
	"""
	def get_query_set(self):
		return super(LiveUpdateManager, self).get_query_set().filter(update_outcome='complete')