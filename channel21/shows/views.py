from shows.models import *
from episodes.models import *
from utils.views import *
from mainsettings.models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from urllib import quote, unquote

# Create your views here.

def create_show(request):
	try:
		values = {}
		errors = {}
		data = {}
		evaluate_char_field(request, "title", 1000, data, values, errors)
		evaluate_char_field(request, "schedule", 1000, data, values, errors, empty = True)
		evaluate_char_field(request, "description", 10000, data, values, errors, empty = True)
		values["background_change"] = "no"
		if "background_change" in request.POST:
			values["background_change"] = request.POST["background_change"]
		errors["background"] = False	
		values["illustration_change"] = "no"
		if "illustration_change" in request.POST:
			values["illustration_change"] = request.POST["illustration_change"]
		errors["illustration"] = False
		if len(data) == 3:
			newshow = Show.objects.create(title = data["title"], schedule = data["schedule"], description = data["description"])
			if "background" in request.FILES:
				values["background"] = "background"
				try:
					newshow.load_image(request.FILES["background"])
				except:
					newshow.delete()
					errors["background"] = True
					return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
			if "illustration" in request.FILES:
				values["illustration"] = "illustration"
				try:
					newshow.load_illustration(request.FILES["illustration"])
				except:
					if newshow.background.__nonzero__():
						newshow.background.delete()
					newshow.delete()
					errors["illustration"] = True
					return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
			return redirect(request.POST["redirect_good_url"])
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
	except:
		return redirect("/")
	
def delete_show(request):
	try:
		if "showid" in request.POST:
			showid = int(request.POST["showid"])
			shows = Show.objects.filter(id = showid)
			if shows.count() != 0:
				cshow = shows[0]
				for episode in Episode.objects.filter(show = cshow):
					episode.show = None
					episode.save()
				for mainsettings in MainSettings.objects.filter(show1 = cshow):
					mainsettings.show1 = None
					mainsettings.save()
				for mainsettings in MainSettings.objects.filter(show2 = cshow):
					mainsettings.show2 = None
					mainsettings.save()
				for mainsettings in MainSettings.objects.filter(show3 = cshow):
					mainsettings.show3 = None
					mainsettings.save()
				for mainsettings in MainSettings.objects.filter(show4 = cshow):
					mainsettings.show4 = None
					mainsettings.save()
				for mainsettings in MainSettings.objects.filter(show5 = cshow):
					mainsettings.show5 = None
					mainsettings.save()
				if cshow.background.__nonzero__():
					cshow.background.delete()
				if cshow.illustration.__nonzero__():
					cshow.illustration.delete()
				cshow.delete()
		return redirect(request.POST["redirect_url"])
	except:
		return redirect("/")
		
def update_show(request):
	try:
		if "showid" in request.POST:
			showid = int(request.POST["showid"])
			shows = Show.objects.filter(id = showid)
			if shows.count() != 0:
				show = shows[0]
				values = {}
				errors = {}
				data = {}
				evaluate_char_field(request, "title", 1000, data, values, errors)
				evaluate_char_field(request, "schedule", 1000, data, values, errors, empty = True)
				evaluate_char_field(request, "description", 10000, data, values, errors, empty = True)
				values["background_change"] = "no"
				if "background_change" in request.POST:
					values["background_change"] = request.POST["background_change"]
				errors["new_background"] = False
				values["illustration_change"] = "no"
				if "illustration_change" in request.POST:
					values["illustration_change"] = request.POST["illustration_change"]
				errors["new_illustration"] = False
				if len(data) == 3:
					show.title = data["title"]
					show.schedule = data["schedule"]
					show.description = data["description"]
					show.save()
					if "background_change" in request.POST:
						background_change = request.POST["background_change"]
						values["background_change"] = background_change
						if background_change == "delete" and show.background.__nonzero__():
							show.background.delete()
						if background_change == "new_background" and "new_background" in request.FILES:
							try:
								show.load_image(request.FILES["new_background"])
							except:
								errors["new_background"] = True
								return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
					else:
						errors["background_change"] = True
					if "illustration_change" in request.POST:
						illustration_change = request.POST["illustration_change"]
						values["illustration_change"] = illustration_change
						if illustration_change == "delete" and show.illustration.__nonzero__():
							show.illustration.delete()
						if illustration_change == "new_illustration" and "new_illustration" in request.FILES:
							try:
								show.load_illustration(request.FILES["new_illustration"])
							except:
								errors["new_illustration"] = True
								return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
					else:
						errors["illustration_change"] = True
					return redirect(request.POST["redirect_good_url"])
				return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : {}, "errors" : {"showid" : True}})))
	except:
		return redirect("/")
		
def create_shot(request):
	try:
		if "showid" in request.POST:
			showid = int(request.POST["showid"])
			shows = Show.objects.filter(id = showid)
			if shows.count() != 0:
				cshow = shows[0]
				if "priority" in request.POST:
					cpriority = int(request.POST["priority"])
					if "shot" in request.FILES:
						try:
							new_shot = Shot.objects.create(show = cshow, priority = cpriority)
							new_shot.load_shot(request.FILES["shot"])
							return redirect(request.POST["redirect_good_url"])
						except:
							return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : {}, "errors" : {"shot" : True}})))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : {}, "errors" : {"showid" : True}})))
	except:
		return redirect("/")
		
def update_shot(request):
	try:
		if "shotid" in request.POST:
			shotid = int(request.POST)
			shots = Shot.objects.filter(id = shotid)
			if shots.count() != 0:
				shot = shots[0]
				if "priority" in request.POST:
					npriority = int(request.POST["priority"])
					shot.priority = npriority
					shot.save()
					return redirect(request.POST["redirect_good_url"])
				return redirect(request.POST["redirect_bad_url"] + "?formstate" + quote(json.dumps({"values" : {}, "errors" : {"priority" : True}})))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : {}, "errors" : {"shotid" : True}})))
	except:
		return redirect("/")
		
def delete_shot(request):
	try:
		if "shotid" in request.POST:
			shotid = int(request.POST["shotid"])
			shots = Shot.objects.filter(id = shotid)
			if shots.count() != 0:
				shot = shots[0]
				shot.delete()
		return redirect(request.POST["redirect_url"])
	except:
		return redirect("/")