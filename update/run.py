import os
import sys

# Load Django config
current_dir = os.path.abspath(__file__)
projects_dir = os.sep.join(current_dir.split(os.sep)[:-2])
data_dir = os.path.join(projects_dir, 'archive', 'html')
os.environ['PYTHONPATH'] = projects_dir
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append(projects_dir)

from update.archive import archive
from update.parse import parse
from update.load import load

from toolbox.dprint import dprint

if __name__ == '__main__':
	soup = archive(data_dir)
	scores_dict, timestamp = parse(soup)
	dprint(scores_dict)
	load(scores_dict, timestamp)