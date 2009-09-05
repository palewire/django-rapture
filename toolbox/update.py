import os
import sys
import re
import time
import datetime
import urllib
from BeautifulSoup import BeautifulSoup

# Load Django config
current_dir = os.path.abspath(__file__)
projects_dir = os.sep.join(current_dir.split(os.sep)[:-2])
data_dir = os.path.join(projects_dir, 'archive', 'html')
os.environ['PYTHONPATH'] = projects_dir
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append(projects_dir)

from django.template.defaultfilters import slugify
from data.models import Category, Edition, Score
from toolbox._mkdir import _mkdir

def text2date(text):
	"""
	Converts the date strings published by Rapture Ready into a datetime.date object.
	"""
	text = text.strip()
	time_tuple = time.strptime(text, '%b %d, %Y')
	return datetime.date(*(time_tuple[0:3]))


def strip_html(text):
	return re.sub(r'<[^>]*?>', '', text)


def parse_score(text):
	"""
	Pulls apart the score provided by Rapture Ready in cases where they include a `+` or a `-`
	to indicate changes from the last list.
	"""
	text = text.strip()
	# Scores range from 1 to 5, so we should expect typical score to only be one character in length.
	# And since we only need that first character, we can just snap it from the rest each time,
	# regardless of how long the string might be.
	return text[0]

def pull():
	"""
	Visits the Rapture Ready Index and scrapes the latest scores.

	Returns a tuple with two things:
	 01. A data dictionary where the keys are entries on the index and the values are their current scores.
	 02. A string with the timestamp as a datetime.datetime object.

	"""
	# Visit the URL and snatch the HTML
	url = 'http://www.raptureready.com/rap2.html'
	http = urllib.urlopen(url)
	soup = BeautifulSoup(http)

	# Save the html in our archive
	now = datetime.datetime.now()
	html_dir = os.path.join(data_dir, str(now.date()), str(now.time()))
	_mkdir(html_dir)
	outfile_path = os.path.join(html_dir, 'rap2.html')
	outfile = open(outfile_path, 'w')
	print >> outfile, soup.prettify()

	# Narrow down to the table containing the rankings
	table = soup.find('table', attrs={
	 'border': '0',
	 'cellspacing': '6',
	})
	# Split the three columns into entries in a list
	column_list = table.findAll('table')
	# Initialize a dictionary for storing the results
	scores_dict = {}
	# Create a regex for picking through the wacky way they print the scores.
	score_regex = re.compile('^\\n<!-(.*)->(?P<score>(.*))$')
	# Loop through the columns
	for column in column_list:
		# Make a list of the entries in the order they appear.
		entries = [li.font.string.strip() for li in column.findAll('li')]
		# Grab the <td> tag that contains the scores.
		scores_table = column.find('td', attrs={'width': '14%'})
		# Smush all the HTML into one big string
		scores_string = "".join(map(str, scores_table.font.contents))
		# Split that HTML on <br> tags and use the regex to snatch out the scores.
		scores = [score_regex.search(i).group('score').strip() for i in scores_string.split('<br />')]
		# Loop through the entries
		for i, entry in enumerate(entries):
			# And assign it with its corresponding score to our data dictionary.
			# Since they occur in the same order, we can use enumerate to pull
			# the same index value from the other set.
			scores_dict[entry] = parse_score(scores[i])

	# Use a regex to snag the line where the update date is published, and then walk up to the parent HTML tag
	timestamp_html = soup.find(text=re.compile('Updated')).parent
	# Smush all the html in the tag into a big string, stripping out the html
	timestamp_string = strip_html("".join(map(str, timestamp_html)))
	# Split the string on 'updated' and grab the other half, stripping out all the whitespace.
	# And then pass it to our conversion function that will translate the string into a date object.
	timestamp = text2date(timestamp_string.split('Updated')[1].strip())

	# Return the dictionary of scores along with the timestamp in a tuple
	return scores_dict, timestamp

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


if __name__ == '__main__':
	data_dict, timestamp = pull()
	from pprint import pprint
	pprint(data_dict)
	#load(data_dict, timestamp)
