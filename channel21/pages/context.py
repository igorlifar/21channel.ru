# -*- coding: utf-8 -*_

from news.models import NewsItem
from episodes.models import Episode
from shows.models import Show
from archive.models import Archive
from schedule.models import Program
from mainsettings.models import MainSettings
from urllib import unquote, quote
import json
from django.http import Http404
from mainsettings.models import MainSettings

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
		
					if "copyfrom" in request.GET:
						newsid = int(request.GET["copyfrom"])
						items = NewsItem.objects.filter(id = newsid)
						if items.count() != 0:
							item = items[0]
							elem = {
								"title" : item.title,
								"preview" : item.preview,
								"text" : item.text,
								"image_change" : "no"
							}
							res["fs"] = {"errors" : {}, "values" : elem}
					
					if 'formstate' in request.GET:
						try:
							res["er"] = True
							res["fs"] = json.loads(unquote(request.GET['formstate']))
						except:
							raise Http404
			
				if s[1] == 'delete-check':
					
					res["id"] = ""
					res["redirect_url"] = ""
					if "id" in request.GET:
						res["id"] = request.GET["id"]
					if "redirect_url" in request.GET:
						res["redirect_url"] = request.GET["redirect_url"]
			
			
		if s[0] == 'episodes':
			if len(s) >= 2:
				if s[1] == 'list':
					res["episodes"] = Episode.objects.all().order_by('-date')
					
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
					
					if "copyfrom" in request.GET:
						episodeid = int(request.GET["copyfrom"])
						episodes = Episode.objects.filter(id = episodeid)
						if episodes.count() != 0:
							episode = episodes[0]
							elem = {
								"title" : episode.title,
								"description" : episode.description,
								"code" : episode.video.code
							}
							if episode.show != None:
								elem.update({"showid" : episode.show.id})
							if episode.video.source == "Y":
								elem.update({"source" : "YouTube"})
							if episode.episodetype == "E":
								elem.update({"episodetype" : "Episode"})
							if episode.episodetype == "I":
								elem.update({"episodetype" : "Issue"})
							if episode.episodetype == "P":
								elem.update({"episodetype" : "Promo"})
							res["fs"] = {"errors" : {}, "values" : elem}
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
						
			
				if s[1] == 'delete-check':
					res["episodeid"] = ""
					res["redirect_url"] = ""
					if "episodeid" in request.GET:
						res["episodeid"] = request.GET["episodeid"]
					if "redirect_url" in request.GET:
						res["redirect_url"] = request.GET["redirect_url"]
 			
		
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
					
					if "copyfrom" in request.GET:
						showid = int(request.GET["copyfrom"])
						shows = Show.objects.filter(id = showid)
						if shows.count() != 0:
							show = shows[0]
							elem = {
								"title" : show.title,
								"description" : show.description,
								"schedule" : show.schedule,
								"background_change" : "no",
								"illustration_change" : "no"
							}
							res["fs"] = {"errors" : {}, "values" : elem}
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
					
				if s[1] == 'delete-check':
					
					res["showid"] = ""
					res["redirect_url"] = ""
					if "showid" in request.GET:
						res["showid"] = request.GET["showid"]
					if "redirect_url" in request.GET:
						res["redirect_url"] = request.GET["redirect_url"]
				
				
		if s[0] == 'archive':
			if len(s) >= 2:
				if s[1] == 'list':
					res["archives"] = Archive.objects.all()
					
				if s[1] == 'edit':
					res["archive"] = Archive.objects.get(id = s[2])
					res["episodesinarchive"] = res["archive"].episodes.all()
					res["episodes"] = []
					for episode in Episode.objects.all().order_by('-date'):
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
						
				if s[1] == 'delete-check':
					res["archiveid"] = ""
					res["redirect_url"] = ""
					if "archiveid" in request.GET:
						res["archiveid"] = request.GET["archiveid"]
					if "redirect_url" in request.GET:
						res["redirect_url"] = request.GET["redirect_url"]
					
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
					
					if "copyfrom" in request.GET:
						programid = int(request.GET["copyfrom"])
						programs = Program.objects.filter(id = programid)
						if programs.count() != 0:
							program = programs[0]
							elem = {
								"title" : program.title,
								"description" : program.description,
								"starttime" : program.starttime,
								"finishtime" : program.finishtime,
								"dayofweek" : program.dayofweek
							}
							res["fs"] = {"errors" : {}, "values" : elem}
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Htpp404
						
				if s[1] == 'delete-check':
					res["programid"] = ""
					res["redirect_url"] = ""
					if "programid" in request.GET:
						res["programid"] = request.GET["programid"]
					if "redirect_url" in request.GET:
						res["redirect_url"] = request.GET["redirect_url"]
		
	return res
	
def get_site_context(s, request):
	res = {}
	
		
	ms = MainSettings.objects.all()[0]
	res["background"] = ms.background
	shows = [
		{
			"title" : ms.show1.title,
			"schedule" : ms.show1.schedule,
			"description" : ms.show1.description,
			"image" : "/media_files/" + ms.show1.illustration.url,
			'id': ms.show1.id
		},
		{
			"title" : ms.show2.title,
			"schedule" : ms.show2.schedule,
			"description" : ms.show2.description,
			"image" : "/media_files/" + ms.show2.illustration.url,
			'id': ms.show2.id
		},
		{
			"title" : ms.show3.title,
			"schedule" : ms.show3.schedule,
			"description" : ms.show3.description,
			"image" : "/media_files/" + ms.show3.illustration.url,
			'id': ms.show3.id
		},
		{
			"title" : ms.show4.title,
			"schedule" : ms.show4.schedule,
			"description" : ms.show4.description,
			"image" : "/media_files/" + ms.show4.illustration.url,
			'id': ms.show4.id
		},
		{
			"title" : ms.show5.title,
			"schedule" : ms.show5.schedule,
			"description" : ms.show5.description,
			"image" : "/media_files/" + ms.show5.illustration.url,
			'id': ms.show5.id
		}
	]
	
	res["shows"] = json.dumps(shows)
	
	programs = []
	
	for i in range(0, 7):
		programs.append([])
		for program in Program.objects.filter(dayofweek = i):
			cur1 = program.starttime.split(":")
			cur2 = program.finishtime.split(":")
			h1 = int(cur1[0])
			m1 = int(cur1[1])
			h2 = int(cur2[0])
			m2 = int(cur2[1])
			if h2 * 60 + m2 < h1 * 60 + m1:
				h2 = h2 + 24
			programs[i].append({
				"title" : program.title,
				"h" : h1,
				"m" : m1,
				"len" : h2 * 60 + m2 - h1 * 60 - m1
			})
		
	res["programs"] = json.dumps(programs)
	
	if s[0] == 'index':
		res['css'] = 'site.css'
		res['js'] = 'site.js'
		
	if s[0] == 'archive':
		if len(s) == 1 or s[1] == 'list':
			res['css'] = 'archive-list.css'
			res['js'] = 'archive-list.js'
			res["archives"] = []
			for archive in Archive.objects.all():
				res["archives"].append({"title" : archive.title, "width" : 225 * archive.episodes.all().count(), "id": archive.id, "episodes" : archive.episodes.all().order_by('-date')})

		else:
			res['css'] = 'archive-category.css'
			res['js'] = 'archive-category.js'
			
			res['cat'] = Archive.objects.get(id=s[1])
			res['eps'] = res['cat'].episodes.all().order_by('-date')
			
	if s[0] == 'episode':
		res['css'] = 'episode.css'
		res['js'] = 'episode.js'
		
		res['ep'] = Episode.objects.get(id=s[1])
		
	if s[0] == 'schedule':
		res['css'] = 'schedule.css'
		res['js'] = 'episode.js'
		
	if s[0] == 'coverage':
		res['css'] = 'coverage.css'
		res['js'] = 'coverage.js'
		
	if s[0] == 'news':
		if len(s) == 1 or s[1] == 'list':
			res['css'] = 'news-list.css'
			res['js'] = 'news-list.js'
			
			res['news'] = NewsItem.objects.all().order_by('-date')

		else:
			res['css'] = 'news-item.css'
			res['js'] = 'news-item.js'
			
			res['m'] = NewsItem.objects.get(id=int(s[1]))
			
	if s[0] == 'shows':
		
		try:
			res['show'] = Show.objects.get(id=s[1])
		except:
			pass
		
		if len(s) == 1 or s[1] == 'list':
			res['css'] = 'shows-list.css'
			res['js'] = 'shows-list.js'
			
			res['shows1'] = Show.objects.all()
			
		elif len(s) == 2:
			res['css'] = 'shows-show.css'
			res['js'] = 'shows-show.js'
			
			res['show'] = Show.objects.get(id=int(s[1]))
			
			sh = Show.objects.get(id=int(s[1]))
			eps = Episode.objects.filter(show=sh).all().order_by('-date')
			
			res['eps'] = eps
			
		elif s[2] == 'episode':
			res['css'] = 'shows-show-episode.css'
			res['js'] = 'shows-show-episode.js'
			
			res['ep'] = Episode.objects.get(id=int(s[3]))
	
	
	return res