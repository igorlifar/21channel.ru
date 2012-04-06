from episodes.models import *
from utils.views import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from urllib import quote, unquote

# Create your views here.

def create_episode(request):
	try:
		values = {}
		errors = {}
		data = {}
		evaluate_char_field(request, "title", 1000, data, values, errors)
		evaluate_char_field(request, "description", 10000, data, values, errors, empty = True)
		evaluate_char_field(request, "source", 100, data, values, errors)
		evaluate_char_field(request, "code", 100, data, values, errors)
		evaluate_char_field(request, "episodetype", 100, data, values, errors)
		if len(data) == 5:
			if data["source"] == "YouTube":
				data["source_value"] = "Y"
			if data["episodetype"] == "Issue":
				data["episodetype_value"] = "I"
			if data["episodetype"] == "Episode":
				data["episodetype_value"] = "E"
			if data["episodetype"] == "Promo":
				data["episodetype_value"] = "P"
			if len(data) == 7:
				if "showid" in request.POST:
					showid = int(request.POST["showid"])
					shows = Show.objects.filter(id = showid)
					if shows.count() != 0:
						data["show"] = shows[0]
				newvideo = Video.objects.create(source = data["source_value"], code = data["code"])
				if len(data) == 7:
					episode = Episode.objects.create(title = data["title"], description = data["description"], video = newvideo)
				else:
					episode = Episode.objects.create(title = data["title"], description = data["description"], video = newvideo, show = data["show"])
				episode.episodetype = data["episodetype_value"]
				episode.save()
				return redirect(request.POST["redirect_good_url"])
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
	except:
		return redirect("/")

def delete_episode(request):
	try:
		if "episodeid" in request.POST:
			episodeid = int(request.POST["episodeid"])
			episodes = Episode.objects.filter(id = episodeid)
			if episodes.count() != 0:
				episode = episodes[0]
				if episode.video != None:
					episode.video.delete()
				episode.delete()
		return redirect(request.POST["redirect_url"])
	except:
		return redirect("/")
		
def update_episode(request):
	try:
		if "episodeid" in request.POST:
			episodeid = int(request.POST["episodeid"])
			episodes = Episode.objects.filter(id = episodeid)
			if episodes.count() != 0:
				episode = episodes[0]
				values = {}
				errors = {}
				data = {}
				evaluate_char_field(request, "title", 1000, data, values, errors)
				evaluate_char_field(request, "description", 10000, data, values, errors, empty = True)
				evaluate_char_field(request, "source", 100, data, values, errors)
				evaluate_char_field(request, "code", 100, data, values, errors)
				evaluate_char_field(request, "episodetype", 100, data, values, errors)
				if len(data) == 5:
					if data["source"] == "YouTube":
						data["source_value"] = "Y"
					if data["episodetype"] == "Issue":
						data["episodetype_value"] = "I"
					if data["episodetype"] == "Episode":
						data["episodetype_value"] = "E"
					if data["episodetype"] == "Promo":
						data["episodetype_value"] = "P"
					if len(data) == 7:
						if "showid" in request.POST:
							showid = int(request.POST["showid"])
							shows = Show.objects.filter(id = showid)
							if shows.count() != 0:
								data["show"] = shows[0]
						if episode.video != None:
							episode.video.delete()
						newvideo = Video.objects.create(source = data["source_value"], code = data["code"])
						episode.video = newvideo
						episode.episodetype = data["episodetype_value"]
						episode.title = data["title"]
						episode.description = data["description"]
						episode.show = None
						if len(data) == 8:
							episode.show = data["show"]
						episode.save()
						return redirect(request.POST["redirect_good_url"])
				return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : {}, "errors" : {"episodeid" : True}})))
	except:
		return redirect("/")