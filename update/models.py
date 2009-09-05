# Helpers
from django.db import models
from django.utils.translation import ugettext_lazy as _


class LiveUpdateManager(models.Manager):
	"""
	Returns the latest live updates.
	
	Example usage:
		
		>>> Update.live.all()
		
	"""
	def get_query_set(self):
		return super(LiveUpdateManager, self).get_query_set().filter(outcome='complete')


class UpdateLog(models.Model):
	"""
	A log of updates.
	"""
	# When the update happened
	start_date = models.DateTimeField(help_text=_('When the update process began.'))
	end_date = models.DateTimeField(help_text=_('When the update process finished.'), null=True, blank=True)
	
	# How the update went
	archive_path = models.CharField(max_length=1000, null=True, blank=True, help_text=_('Where the files harvested by the scrape are stored.'))
	OUTCOME_CHOICES = (
		('incomplete', 'incomplete'),
		('complete', 'complete'),
	)
	outcome = models.CharField(max_length=20, default='incomplete', choices=OUTCOME_CHOICES, help_text=_('How the update turned out.'))
	loaded_new_data = models.NullBooleanField(default=None, help_text=_('Indicates whether the update loaded any new data to our database.'))
	
	# Meta
	created = models.DateTimeField(auto_now_add=True, editable=False)
	last_updated = models.DateTimeField(auto_now=True, editable=False)
	
	# Managers
	live = LiveUpdateManager()
	
	class Meta:
		db_table = 'rapture_update_log'
		get_latest_by = 'update_end_date'