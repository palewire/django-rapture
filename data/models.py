# Helpers
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Signals
from django.db.models import signals
from data.signals import count_scores


class Category(models.Model):
	"""
	A indicator of the rapture listed on the Rapture Index.
	"""
	name = models.CharField(max_length=20, primary_key=True, help_text=_('The name of the category'))
	slug = models.SlugField(unique=True, help_text=_('A stripped version of the name for URL strings'))
	explanation = models.TextField(help_text=_('An explanation of the category provided by the editors of Rapture Ready.'))

	class Meta:
		ordering = ['name']
		verbose_name = _('categories')

	def __unicode__(self):
		return self.name


class Edition(models.Model):
	"""
	A release of the Rapture Index
	"""
	date = models.DateField(verbose_name=_('Publication date of this edition of the Rapture Index.'))
	total = models.IntegerField(default=0, editable=False, verbose_name=_('The total Rapture Index score from this edition.'))

	class Meta:
		ordering = ['-date']
		get_latest_by = ['-date']

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
	comment = models.TextField(help_text=_('An explanation of this score given by the editors of Rapture Ready.'))

	class Meta:
		ordering = ('edition', )

	def __unicode__(self):
		return u'%s - %s - %s' % (str(self.edition.date), self.category.name, self.score)

# Rerun the totals for each Edition whenever a Score is saved or deleted.
signals.post_save.connect(count_scores, sender=Score)
signals.post_delete.connect(count_scores, sender=Score)
