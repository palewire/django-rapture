from django.template.defaultfilters import slugify
from data.models import Category, Edition, Score

def load(data_dict, timestamp):
	"""
	Accepts the results of the pull function and loads them into our Django models.
	"""
	loaded_new_data = False

	# Load the Edition
	edition_obj, edition_created = Edition.objects.get_or_create(
		date = timestamp
	)
	if edition_created:
		loaded_new_data = True

	for category, score in data_dict.items():
		# Load the categories
		category_obj, category_created = Category.objects.get_or_create(
			name=category,
			slug=slugify(category)
		)
		if category_created:
			loaded_new_data = True

		# Load the scores
		score_obj, score_created = Score.objects.get_or_create(
			edition=edition_obj,
			category=category_obj,
			score=score
		)
		if score_created:
			loaded_new_data = True
			
	return loaded_new_data