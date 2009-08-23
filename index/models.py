from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.db.models import signals
from index.signals import count_scores


class Category(models.Model):
	name = models.CharField(max_length=20, primary_key=True, help_text=_('The name of the category'))
	slug = models.SlugField(unique=True, help_text=_('A stripped version of the name for URL strings'))

	class Meta:
		ordering = ['name']
		verbose_name_plural = _('categories')

	def __unicode__(self):
		return self.name


class Edition(models.Model):
	date = models.DateField(verbose_name=_('Publication date of this edition of the Rapture Index'))
	total = models.IntegerField(default=0, editable=False, verbose_name=_('The total Rapture Index score from this edition.'))

	class Meta:
		ordering = ['-date']
		get_latest_by = ['-date']

	def __unicode__(self):
		return u'%s (%s)'  % (str(self.date), self.total)

	def get_total(self):
		return sum([i.score for i in self.score_set.all()])


class Score(models.Model):
	edition = models.ForeignKey(Edition, help_text=_('The edition this score was released.'))
	category = models.ForeignKey(Category, help_text=_('The category this score is for.'))
	score = models.IntegerField(help_text=_('The score, ranging from 1-5'))

	def __unicode__(self):
		return u'%s - %s - %s'	% (str(self.edition.date), self.category.name, self.score)

# Rerun the totals for each Edition whenever a Score is saved or deleted.
signals.post_save.connect(count_scores, sender=Score)
signals.post_delete.connect(count_scores, sender=Score)
