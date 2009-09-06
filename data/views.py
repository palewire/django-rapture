# Utils
import os
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.simple import direct_to_template

# Models
from update.models import *
from data.models import *


def csv(request):
	score_list = Score.objects.all()
	context = {'score_list': score_list}
	return render_to_response('scores.csv', context, mimetype="text/javascript")

def json(request):
	score_list = Score.objects.all()
	context = {'score_list': score_list}
	return render_to_response('scores.json', context, mimetype="text/javascript")

def xml(request):
	score_list = Score.objects.all()
	context = {'score_list': score_list}
	return render_to_response('scores.xml', context, mimetype="text/javascript")