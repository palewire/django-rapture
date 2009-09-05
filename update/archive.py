import os
import sys
import datetime
import urllib
from BeautifulSoup import BeautifulSoup
from toolbox._mkdir import _mkdir

def archive(data_dir):
	"""
	Visits the Rapture Ready Index and archive the site.

	Returns a BeautifulSoup object with the HTML in it.
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
	
	# Create a list of all the resources the page calls
	# that we want to download so we can recreate it later.
	resources = []
	
	# Images
	for img in soup.findAll("img", {"src":True}):
		resources.append(img["src"])
		
	# Cascading Style Sheets
	for link in soup.findAll("link", {"rel":"stylesheet", "type":"text/css"}):
		resources.append(link["href"])

	# Alternative Cascading Style Sheets
	for link in soup.findAll("link", {"rel":"alternate stylesheet", "type":"text/css"}):
		resources.append(link["href"])
		
	# Download all the images to the archive.
	for r in resources:
		# Split the relative path to the img
		head, tail = os.path.split(r)

		# Create a directory to store the file
		r_dir = os.path.join(html_dir, head)
		_mkdir(r_dir)
		
		# Path together an absolute URL we can download
		url = 'http://www.raptureready.com' + r
		local_path = os.path.join(r_dir, tail)
		urllib.urlretrieve(url, local_path)
		
	return soup
	
if __name__ == '__main__':
	html_path = archive()