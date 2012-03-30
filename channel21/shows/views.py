from shows.models import *
from episodes.models import *
from utils.views import *
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
		evaluate_char_field(request, "schedule", 1000, data, values, errors)
		evaluate_char_field(request, "description", 10000, data, values, errors)
		if len(data) == 3:
			newshow = Show.objects.create(title = data["title"], schedule = data["schedule"], description = data["description"])
			values["background"] = False
			errors["background"] = False
			if "background" in request.FILES:
				values["background"] = True
				try:
					newshow.load_image(request.FILES["background"])
				except:
					newshow.delete()
					errors["background"] = True
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
				if cshow.background.__nonzero__():
					cshow.background.delete()
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
				evaluate_char_field(request, "schedule", 1000, data, values, errors)
				evaluate_char_field(request, "description", 10000, data, values, errors)
				if len(data) == 3:
					show.title = data["title"]
					show.schedule = data["schedule"]
					show.description = data["description"]
					show.save()
					errors["background_change"] = False
					if "background_change" in request.POST:
						background_change = request.POST["background_change"]
						values["background_change"] = background_change
						if background_change == "delete" and show.background.__nonzero__():
							show.background.delete()
						values["new_background"] = False
						errors["new_background"] = False
						if background_change == "new_background" and "new_background" in request.FILES:
							values["new_background"] = True
							try:
								show.load_image(request.FILES["new_background"])
							except:
								errors["new_background"] = True
								return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
					else:
						errors["background_change"] = True
					return redirect(request.POST["redirect_good_url"])
				return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : {}, "errors" : {"showid" : True}})))
	except:
		return redirect("/")