# Helpers
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import truncate_words
from django.template.defaultfilters import date as date_format

# Signals
from django.db.models import signals
from data.signals import count_scores


class Category(models.Model):
	"""
	A indicator of the rapture listed on the Rapture Index.
	"""
	name = models.CharField(max_length=20, primary_key=True, help_text=_('The name of the category'))
	slug = models.SlugField(unique=True, help_text=_('A stripped version of the name for URL strings'))
	explanation = models.TextField(help_text=_('An explanation of the category provided by the editors of Rapture Ready.'), null=True, blank=True)
	# Meta
	created = models.DateTimeField(auto_now_add=True, editable=False)
	last_updated = models.DateTimeField(auto_now=True, editable=False)

	class Meta:
		ordering = ['name']
		verbose_name_plural = _('categories')
		db_table = 'rapture_data_category'

	def __unicode__(self):
		return self.name

	def get_short_explanation(self, words=10):
		return truncate_words(self.explanation, words)
	short_explanation = property(get_short_explanation)


class Edition(models.Model):
	"""
	A release of the Rapture Index
	"""
	date = models.DateField(verbose_name=_('Publication date of this edition of the Rapture Index.'))
	total = models.IntegerField(default=0, editable=False, verbose_name=_('The total Rapture Index score from this edition.'))
	# Meta
	created = models.DateTimeField(auto_now_add=True, editable=False)
	last_updated = models.DateTimeField(auto_now=True, editable=False)

	class Meta:
		ordering = ['-date']
		get_latest_by = ['-date']
		db_table = 'rapture_data_edition'

	def __unicode__(self):
		return u'%s (%s)'  % (str(self.date), self.total)

	def get_total(self):
		return sum([i.score for i in self.score_set.all()])


class Score(models.Model):
	"""
	The score registered by an Indicator in a particular Edition.
	"""
	edition = models.ForeignKey(Edition, help_text=_('The edition this score was released.'))
	category = models.ForeignKey(Category, help_text=_('The indicator this score is for.'))
	score = models.IntegerField(help_text=_('The score, ranging from 1-5'))
	comment = models.TextField(help_text=_('An explanation of this score given by the editors of Rapture Ready.'), null=True, blank=True)
	# Meta
	created = models.DateTimeField(auto_now_add=True, editable=False)
	last_updated = models.DateTimeField(auto_now=True, editable=False)

	class Meta:
		ordering = ('category', 'edition')
		db_table = 'rapture_data_score'

	def __unicode__(self):
		return u'%s: %s (%s)' % (self.category.name, self.score, date_format(self.edition.date, 'N d, Y'))


# Rerun the totals for each Edition whenever a Score is saved or deleted.
signals.post_save.connect(count_scores, sender=Score)
signals.post_delete.connect(count_scores, sender=Score)
