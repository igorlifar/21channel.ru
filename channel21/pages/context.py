# -*- coding: utf-8 -*_

from news.models import NewsItem
from episodes.models import Episode
from shows.models import Show
from archive.models import Archive
from schedule.models import Program
from mainsettings.models import MainSettings
from urllib import unquote
import json
from django.http import Http404

def get_panel_context(s, request):

	res = {
		"static": "/static_files/"
	}
	
	if request.user.is_anonymous():
		res["user"] = {
			"anonymous": True
		}
	else:
		res["user"] = {
			'anonymous': False,
			'name': request.user.first_name + ' ' + request.user.last_name
		}
		
	if len(s) >= 1:
		
		if s[0] == 'settings':
			if len(s) >= 2:
				if s[1] == 'list':
					res["settings"] = MainSettings.objects.get(id = 1)
				
				if s[1] == 'edit':
					res["settings"] = MainSettings.objects.get(id = 1)
					res["shows"] = Show.objects.all()
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
		
		if s[0] == 'news':
			if len(s) >= 2:
				if s[1] == 'list':
					res["news"] = NewsItem.objects.all()
				
				if s[1] == 'edit':
					res["news_item"] = NewsItem.objects.get(id=s[2])
					
					if 'formstate' in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET['formstate']))
						except:
							raise Http404
					
				if s[1] == 'add':
					if 'formstate' in request.GET:
						try:
							res["er"] = True
							res["fs"] = json.loads(unquote(request.GET['formstate']))
						except:
							raise Http404
			
		if s[0] == 'episodes':
			if len(s) >= 2:
				if s[1] == 'list':
					res["episodes"] = Episode.objects.all()
					
				if s[1] == 'edit':
					res["episode"] = Episode.objects.get(id = s[2])
					res["shows"] = Show.objects.all()
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
				
				if s[1] == 'add':
					res["shows"] = Show.objects.all()
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
		
		if s[0] == 'shows':
			if len(s) >= 2:
				if s[1] == 'list':
					res["shows"] = Show.objects.all()
					
				if s[1] == 'edit':
					res["show"] = Show.objects.get(id = s[2])
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
						
				if s[1] == 'add':
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
					
		if s[0] == 'archive':
			if len(s) >= 2:
				if s[1] == 'list':
					res["archives"] = Archive.objects.all()
					
				if s[1] == 'edit':
					res["archive"] = Archive.objects.get(id = s[2])
					res["episodesinarchive"] = res["archive"].episodes.all()
					res["episodes"] = []
					for episode in Episode.objects.all():
						if res["episodesinarchive"].filter(id = episode.id).count() == 0:
							res["episodes"].append(episode)
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
				
				if s[1] == 'add':
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
					
		if s[0] == 'schedule':
			if len(s) >= 2:
				if s[1] == 'list':
					res["week"] = [
						{"id" : 0, "title" : u"Понедельник"}, 
						{"id" : 1, "title" : u"Вторник"}, 
						{"id" : 2, "title" : u"Среда"},
						{"id" : 3, "title" : u"Четверг"},
						{"id" : 4, "title" : u"Пятница"},
						{"id" : 5, "title" : u"Суббота"},
						{"id" : 6, "title" : u"Воскресенье"}
					]
					for day in res["week"]:
						day["programs"] = Program.objects.filter(dayofweek = day["id"])
						
				if s[1] == 'edit':
					res["program"] = Program.objects.get(id = s[2])
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
						
				if s[1] == 'add':
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Htpp404
		
	return res
	
def get_site_context(section, request):
	res = {}
	
	return res