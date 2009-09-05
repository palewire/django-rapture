from django.template.defaultfilters import slugify
from data.models import Category, Edition, Score

def load(data_dict, timestamp):
	"""
	Accepts the results of the pull function and loads them into our Django models.
	"""

	# Load the Edition
	edition_obj, edition_created = Edition.objects.get_or_create(
		date = timestamp
	)
	if edition_created:
		print "Added edition %s" % str(edition_obj.date)

	for category, score in data_dict.items():
	# Load the categories
		category_obj, category_created = Category.objects.get_or_create(
		name=category,
		slug=slugify(category)
	)
	if category_created:
		print "Added category %s" % category_obj.name

	# Load the scores
	score_obj, score_created = Score.objects.get_or_create(
		edition=edition_obj,
		category=category_obj,
		score=score
	)
	if score_created:
		print "Added score %s" % score_obj