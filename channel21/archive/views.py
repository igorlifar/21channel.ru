from archive.models import *
from episodes.models import *
from utils.views import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from urllib import quote, unquote

# Create your views here.

def create_archive(request):
	try:
		values = []
		errors = []
		data = {}
		evaluate_char_field(request, "title", 1000, data, values, errors)
		if len(data) == 1:
			archive = Archive.objects.create(title = data["title"])
			archive.save()
			return redirect(request.POST["redirect_good_url"])
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
	except:
		return redirect("/")
		
def delete_archive(request):
	try:
		if "archiveid" in request.POST:
			archiveid = int(request.POST["archiveid"])
			archives = Archive.objects.filter(id = archiveid)
			if archives.count() != 0:
				archive = archives[0]
				archive.episodes.clear()
				archive.delete()
		return redirect(request.POST["redirect_url"])
	except:
		return redirect("/")
	
def update_archive(request):
	try:
		if "archiveid" in request.POST:
			archiveid = int(request.POST["archiveid"])
			archives = Archive.objects.filter(id = archiveid)
			if archives.count() != 0:
				archive = archives[0]
				values = []
				errors = []
				data = {}
				evaluate_char_field(request, "title", 1000, data, values, errors)
				if len(data) == 1:
					archive.title = data["title"]
					archive.save()
					return redirect(request.POST["redirect_good_url"])
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : [], "errors" : ["archiveid"]})))
	except:
		return redirect("/")

def add_episode_to_archive(request):
	try:
		if "archiveid" in request.POST:
			archiveid = int(request.POST["archiveid"])
			archives = Archive.objects.filter(id = archiveid)
			if archives.count() != 0:
				archive = archives[0]
				if "episodeid" in request.POST:
					episodeid = int(request.POST["episodeid"])
					episodes = Episode.objects.filter(id = episodeid)
					if episodes.count() != 0:
						episode = episodes[0]
						if archive.episodes.filter(id = episode.id).count() == 0:
							archive.episodes.add(episode)
						return redirect(request.POST["redirect_good_url"])
				return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : [], "errors" : ["episodeid"]})))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : [], "errors" : ["archiveid"]})))
	except:
		return redirect("/")
	
def delete_episode_from_archive(request):
	try:
		if "archiveid" in request.POST:
			archiveid = int(request.POST["archiveid"])
			archives = Archive.objects.filter(id = archiveid)
			if archives.count() != 0:
				archive = archives[0]
				if "episodeid" in request.POST:
					episodeid = int(request.POST["episodeid"])
					episodes = Episode.objects.filter(id = episodeid)
					if episodes.count() != 0:
						episode = episodes[0]
						if archive.episodes.filter(id = episode.id).count() != 0:
							archive.episodes.remove(episode)
						return redirect(request.POST["redirect_good_url"])
				return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : [], "errors" : ["episodeid"]})))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : [], "errors" : ["archiveid"]})))	
	except:
		return redirect("/")
