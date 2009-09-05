import os
import sys
import re
import time
import datetime
import urllib
from BeautifulSoup import BeautifulSoup

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


def parse(soup):
	
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
	