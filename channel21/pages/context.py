# -*- coding: utf-8 -*_

from news.models import NewsItem
from episodes.models import Episode
from shows.models import Show, Shot, Article, MetaItem
from archive.models import Archive
from schedule.models import Program
from mainsettings.models import MainSettings, LocalSettings
from urllib import unquote, quote
import json
from django.http import Http404
from mainsettings.models import MainSettings
from comments.models import *
from staticpages.models import Category, Page
from profiling import profile
from geolocation.models import *
from django_geoip.models import *
from django_geoip.views import *

def get_panel_context(s, request):

	res = {
		"static": "/static_files/",
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
		if s[0] == 'index':
			res["ep_count"] = Episode.objects.all().count()
			res["show_count"] = Show.objects.all().count()
			res["archive_count"] = Archive.objects.all().count()
			res["news_count"] = NewsItem.objects.all().count()
			
		if s[0] == 'settings':
			if len(s) >= 2:
				if s[1] == 'list':
					res["settings"] = MainSettings.objects.get(id = 1)
				
				if s[1] == 'edit':
					res["settings"] = MainSettings.objects.get(id = 1)
					res["shows"] = Show.objects.all()
					
					if "success" in request.GET:
						res["success"] = True
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
		
				if s[1] == 'edit-local':
					if "regionid" in request.GET:
						try:
							region = geoLocation.objects.get(id = request.GET["regionid"])
							lsettings = LocalSettings.objects.get(region = region)
							res["region"] = {
								"id" : region.id,
								"name" : region.region.name,
								"show1" : lsettings.show1,
								"show2" : lsettings.show2,
								"show3" : lsettings.show3,
								"show4" : lsettings.show4,
								"show5" : lsettings.show5,
							}
						except:
							res["region"] = None
					regions = geoLocation.objects.all()
					res["regions"] = []
					for r in regions:
						current = {
							"id" : r.id,
							"name" : r.region.name
						}
						res["regions"].append(current)
					res["shows"] = Show.objects.all()
					
					if "success" in request.GET:
						res["success"] = True
						
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
					
					if "success" in request.GET:
						res["success"] = True
					
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
					allepisodes = Episode.objects.all().order_by('-date')
					res["episodes"] = []
					if "page" in request.GET:
						res["lastpage"] = int((allepisodes.count() + 24) / 25)
						res["lastpage2"] = res["lastpage"] - 1
						res["page"] = int(request.GET["page"])
						if res["page"] < 1 or res["page"] > res["lastpage"]:
							res["page"] = 1
						res["prevpage"] = res["page"] - 1
						res["nextpage"] = res["page"] + 1
						size1 = 0
						size2 = 0
						for episode in allepisodes:
							if size1 == (res["page"] - 1) * 25:
								res["episodes"].append(episode)
								size2 = size2 + 1
								if size2 == 25:
									break
								continue
							size1 = size1 + 1
					else:
						size = 0
						for episode in allepisodes:
							res["episodes"].append(episode)
							size = size + 1
							if size == 25:
								break
						res["page"] = 1
						res["prevpage"] = 0
						res["nextpage"] = 2
						res["lastpage"] = int((allepisodes.count() + 24) / 25)
						res["lastpage2"] = res["lastpage"] - 1
					
				if s[1] == 'edit':
					res["episode"] = Episode.objects.get(id = s[2])
					res["shows"] = Show.objects.all()
					
					if "success" in request.GET:
						res["success"] = True
					
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
				
				if s[1] == "list-shots":
					res["show"] = Show.objects.get(id = s[2])
					res["shots"] = Shot.objects.filter(show = res["show"])
				
				if s[1] == "add-shot":
					res["show"] = Show.objects.get(id = s[2])
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
						
				if s[1] == "edit-shot":
					res["shot"] = Shot.objects.get(id = s[2])
					res["show"] = Show.objects.get(id = res["shot"].show.id)
					
					if "success" in request.GET:
						res["success"] = True
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
						
				if s[1] == "delete-shot":
					
					res["shotid"] = ""
					res["redirect_url"] = ""
					if "shotid" in request.GET:
						res["shotid"] = request.GET["shotid"]
					if "redirect_url" in request.GET:
						res["redirect_url"] = request.GET["redirect_url"]
				
				if s[1] == "list-articles":
					res["show"] = Show.objects.get(id = s[2])
					res["articles"] = Article.objects.filter(show = res["show"])
					
				if s[1] == "add-article":
					res["show"] = Show.objects.get(id = s[2])
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
						
				if s[1] == "edit-article":
					res["article"] = Article.objects.get(id = s[2])
					res["show"] = Show.objects.get(id = res["article"].show.id)
					
					if "success" in request.GET:
						res["success"] = True
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
						
				if s[1] == "delete-article":
					
					res["articleid"] = ""
					res["redirect_url"] = ""
					if "articleid" in request.GET:
						res["articleid"] = request.GET["articleid"]
					if "redirect_url" in request.GET:
						res["redirect_url"] = request.GET["redirect_url"]
				
				if s[1] == "list-meta":
					res["show"] = Show.objects.get(id = s[2])
					res["metaitems"] = MetaItem.objects.filter(show = res["show"])
				
				if s[1] == "add-meta":
					res["show"] = Show.objects.get(id = s[2])
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
						
				if s[1] == "edit-meta":
					res["metaitem"] = MetaItem.objects.get(id = s[2])
					res["show"] = Show.objects.get(id = res["metaitem"].show.id)
					
					if "success" in request.GET:
						res["success"] = True
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
						
				if s[1] == "delete-meta":
					
					res["metaitemid"] = ""
					res["redirect_url"] = ""
					if "metaitemid" in request.GET:
						res["metaitemid"] = request.GET["metaitemid"]
					if "redirect_url" in request.GET:
						res["redirect_url"] = request.GET["redirect_url"]
				
				if s[1] == 'list':
					res["shows"] = Show.objects.all()
					
				if s[1] == 'edit':
					res["show"] = Show.objects.get(id = s[2])
					
					if "success" in request.GET:
						res["success"] = True
					
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
					
					if "success" in request.GET:
						res["success"] = True
					
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
						day["programs"] = Program.objects.filter(dayofweek = day["id"], region = None)
						
				if s[1] == 'local':
					res["week"] = [
						{"id" : 0, "title" : u"Понедельник"}, 
						{"id" : 1, "title" : u"Вторник"}, 
						{"id" : 2, "title" : u"Среда"},
						{"id" : 3, "title" : u"Четверг"},
						{"id" : 4, "title" : u"Пятница"},
						{"id" : 5, "title" : u"Суббота"},
						{"id" : 6, "title" : u"Воскресенье"}
					]
					if "regionid" in request.GET:
						try:
							region = geoLocation.objects.get(id = request.GET["regionid"])
							res["region"] = {
								"id" : region.id,
								"name" : region.region.name
							}
							for day in res["week"]:
								day["programs"] = Program.objects.filter(dayofweek = day["id"], region = region)
						except:
							res["region"] = None
						
					res["regions"] = []
					for r in geoLocation.objects.all():
						current = {
							"id" : r.id,
							"name" : r.region.name
						}
						res["regions"].append(current)
						
				if s[1] == 'local-add':
					
					res["regions"] = []
					for r in geoLocation.objects.all():
						current = {
							"id" : r.id,
							"name" : r.region.name
						}
						res["regions"].append(current)
					
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Htpp404
						
				if s[1] == 'local-edit':
					res["program"] = Program.objects.get(id = s[2])
					
					res["regions"] = []
					for r in geoLocation.objects.all():
						current = {
							"id" : r.id,
							"name" : r.region.name
						}
						res["regions"].append(current)
					
					if "success" in request.GET:
						res["success"] = True
						
					if "formstate" in request.GET:
						try:
							res["fs"] = json.loads(unquote(request.GET["formstate"]))
						except:
							raise Http404
						
				if s[1] == 'edit':
					res["program"] = Program.objects.get(id = s[2])
					
					if "success" in request.GET:
						res["success"] = True
					
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
					
		if s[0] == 'pages':
			
			if s[1] == 'list':
				res["categories"] = Category.objects.all().order_by("-priority")
				
			if s[1] == 'add' or s[1] == 'edit':
				res["categories"] = Category.objects.all().order_by("-priority")
				
			if s[1] == 'add':
				
				if "formstate" in request.GET:
					try:
						res["fs"] = json.loads(unquote(request.GET["formstate"]))
					except:
						raise Http404
					
			if s[1] == 'edit':
				
				res["page"] = Page.objects.get(id = s[2])
				
				if "success" in request.GET:
					res["success"] = True
					
				if "formstate" in request.GET:
					try:
						res["fs"] = json.loads(unquote(request.GET["formstate"]))
					except:
						raise Http404
					
			if s[1] == 'delete-check':
				res["pageid"] = ""
				res["redirect_url"] = ""
				if "pageid" in request.GET:
					res["pageid"] = request.GET["pageid"]
				if "redirect_url" in request.GET:
					res["redirect_url"] = request.GET["redirect_url"]
			
		if s[0] == 'regions':
			
			if s[1] == 'list':
				res["regions"] = []
				for r in geoLocation.objects.all():
					current = {
						"id" : r.id,
						"name" : r.region.name,
						"is_default" : r.is_default
					}
					res["regions"].append(current)
					
			if s[1] == 'add':
				res["allregions"] = []
				for r in Region.objects.all():
					if geoLocation.objects.filter(region = r).count() != 0:
						continue
					current = {
						"id" : r.id,
						"name" : r.name
					}
					res["allregions"].append(current)
			
				if "formstate" in request.GET:
					try:
						res["fs"] = json.loads(unquote(request.GET["formstate"]))
					except:
						raise Http404
			
			if s[1] == 'delete-check':
				res["regionid"] = ""
				res["redirect_url"] = ""
				if "regionid" in request.GET:
					res["regionid"] = request.GET["regionid"]
				if "redirect_url" in request.GET:
					res["redirect_url"] = request.GET["redirect_url"]
			
	return res
	


@profile('get_site_context')
def get_site_context(s, request):
	
	res = {}
	
	res['request'] = request
	res['user'] = request.user
	res['ulogin_user'] = None

	res['footer_cats'] = Category.objects.all().order_by("-priority")[:3]
	
	try:
		res['ulogin_user'] = request.user.ulogin_users.all()[0]
	except:
		pass
		
	ms = MainSettings.objects.all()[0]
	res["regions"] = []
	for r in geoLocation.objects.all():
		current = {
			"id" : r.id,
			"name" : r.region.name
		}
		res["regions"].append(current)
	res["region"] = {
		"id" : request.location.id,
		"name" : request.location.region.name
	}
	res["pageurl"] = request.path
	res["background"] = ms.background
	shows = []
	if ms.show1 != None:
		current = {
			"title" : ms.show1.title,
			"schedule" : ms.show1.schedule,
			"description" : ms.show1.description,
			"image" : ms.show1.illustration.url,
			'id': ms.show1.id
		}
		shows.append(current)
	if ms.show2 != None:
		current = {
			"title" : ms.show2.title,
			"schedule" : ms.show2.schedule,
			"description" : ms.show2.description,
			"image" : ms.show2.illustration.url,
			'id': ms.show2.id
		}
		shows.append(current)
	if ms.show3 != None:
		current = {
			"title" : ms.show3.title,
			"schedule" : ms.show3.schedule,
			"description" : ms.show3.description,
			"image" : ms.show3.illustration.url,
			'id': ms.show3.id
		}
		shows.append(current)
	if ms.show4 != None:
		current = {
			"title" : ms.show4.title,
			"schedule" : ms.show4.schedule,
			"description" : ms.show4.description,
			"image" : ms.show4.illustration.url,
			'id': ms.show4.id
		}
		shows.append(current)
	if ms.show5 != None:
		current = {
			"title" : ms.show5.title,
			"schedule" : ms.show5.schedule,
			"description" : ms.show5.description,
			"image" : ms.show5.illustration.url,
			'id': ms.show5.id
		}
		shows.append(current)
	
	ls = LocalSettings.objects.get(region = request.location)
	
	localshows = []
	
	if request.location.is_default:
		localshows = shows
	else:
		if ls.show1 != None:
			localshows.append({
				"title" : ls.show1.title,
				"schedule" : ls.show1.schedule,
				"description" : ls.show1.description,
				"image" : ls.show1.illustration.url,
				'id': ls.show1.id
			})
		if ls.show2 != None:
			localshows.append({
				"title" : ls.show2.title,
				"schedule" : ls.show2.schedule,
				"description" : ls.show2.description,
				"image" : ls.show2.illustration.url,
				'id': ls.show2.id
			})
		if ls.show3 != None:
			localshows.append({
				"title" : ls.show3.title,
				"schedule" : ls.show3.schedule,
				"description" : ls.show3.description,
				"image" : ls.show3.illustration.url,
				'id': ls.show3.id
			})
		if ls.show4 != None:
			localshows.append({
				"title" : ls.show4.title,
				"schedule" : ls.show4.schedule,
				"description" : ls.show4.description,
				"image" : ls.show4.illustration.url,
				'id': ls.show4.id
			})
		if ls.show5 != None:
			localshows.append({
				"title" : ls.show5.title,
				"schedule" : ls.show5.schedule,
				"description" : ls.show5.description,
				"image" : ls.show5.illustration.url,
				'id': ls.show5.id
			})
	
	res["shows"] = json.dumps(shows)
	res["localshows"] = json.dumps(localshows)
	
	programs = []
	
	for i in range(0, 7):
		programs.append([])
		lst = []
		if request.location.is_default:
			lst = Program.objects.filter(dayofweek = i, region = None)
		else:
			lst = Program.objects.filter(dayofweek = i, region = request.location)
		for program in lst:
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
		
		res["lastepisodes"] = Episode.objects.order_by('-date')[:20]
		res["lastnews"] = NewsItem.objects.order_by('-date')[:20]
		
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
		
		# Show page:
		elif len(s) == 2 or s[2] == 'promo':
			res['css'] = 'shows-show.css'
			res['js'] = 'shows-show.js'
			
			res['show'] = Show.objects.get(id=int(s[1]))
			
			sh = Show.objects.get(id=int(s[1]))
			
			res['comments'] = ShowComment.objects.filter(show=sh).order_by('-date')
			res['meta'] = MetaItem.objects.filter(show=sh).order_by('-priority')
			res['shots'] = Shot.objects.filter(show=sh).order_by('-priority')
			res['shots_count'] = Shot.objects.filter(show=sh).count()
			res['shots_width'] = Shot.objects.filter(show=sh).count() * 109 - 5
			res['articles'] = Article.objects.filter(show=sh, articletype='A').order_by('-priority')
			res['reviews'] = Article.objects.filter(show=sh, articletype='R').order_by('-priority')
			
			res["videos"] = {
				"promo": Episode.objects.filter(show=sh, episodetype="P").order_by('-date'),
				"issues": Episode.objects.filter(show=sh, episodetype="I").order_by('-date')[0:50],
				"episodes": Episode.objects.filter(show=sh, episodetype="E").order_by('-date')[0:50]
			}
			
			if len(s) > 2:
				res['video'] = Episode.objects.get(id=int(s[4]), episodetype='P', show=sh)
		
		elif s[2] == 'episodes':
			sh = Show.objects.get(id=int(s[1]))
			res['css'] = 'shows-show-episodes.css'
			res['js'] = 'shows-show-episodes.js'
			
			res['eps'] = Episode.objects.filter(show=sh, episodetype="E").order_by('-date')
			res['sectiontitle'] = u'Эпизоды'
			
			if len(s) == 5:
				res['video'] = Episode.objects.get(show=sh, episodetype='E', id=int(s[4]))
			
		elif s[2] == 'issues':
			sh = Show.objects.get(id=int(s[1]))
			res['css'] = 'shows-show-episodes.css'
			res['js'] = 'shows-show-episodes.js'
			
			res['eps'] = Episode.objects.filter(show=sh, episodetype="I").order_by('-date')
			res['sectiontitle'] = u'Выпуски'
			
			if len(s) == 5:
				res['video'] = Episode.objects.get(show=sh, episodetype='I', id=int(s[4]))
			
		elif s[2] == 'watch':
			res['css'] = 'shows-show-watch.css'
			res['js'] = 'shows-show-watch.js'
			
			res['ep'] = Episode.objects.get(id=int(s[3]))

	if s[0] == 'pages':
		res['page'] = Page.objects.get(id=s[1])
		res['css'] = 'page.css'
		res['js'] = 'page.js'
	
	
	return res
	