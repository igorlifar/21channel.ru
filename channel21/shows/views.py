from shows.models import *
from utils.views import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response

# Create your views here.

def create_show(request):
	try:
		values = []
		errors = []
		data = {}
		evaluate_char_field(request, "title", 1000, data, values, errors)
		evaluate_char_field(request, "schedule", 1000, data, values, errors)
		evaluate_char_field(request, "description", 10000, data, values, errors)
		if len(data) == 3:
			newshow = Show.objects.create(title = data["title"], schedule = data["schedule"], description = data["description"])
			newshow.save()
			if "background" in request.FILES:
				newshow.load_image(request.FILES["background"])
			return redirect(request.POST["redirect_good_url"])
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + json.dumps({"values" : values, "errors" : errors}))
	except:
		return redirect("/")
	
def delete_show(request):
	try:
		if "showid" in request.POST:
			showid = int(request.POST["showid"])
			shows = Show.objects.filter(id = showid)
			if shows.count() != 0:
				show = shows[0]
				if show.background.__nonzero__():
					show.background.delete()
				show.delete()
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
				values = []
				errors = []
				data = {}
				evaluate_char_field(request, "title", 1000, data, values, errors)
				evaluate_char_field(request, "schedule", 1000, data, values, errors)
				evaluate_char_field(request, "description", 10000, data, values, errors)
				if len(data) == 3:
					show.title = data["title"]
					show.schedule = data["schedule"]
					show.description = data["description"]
					show.save()
					if "background" in request.FILES:
						show.load_image(request.FILES["background"])
					return redirect(request.POST["redirect_good_url"])
				return redirect(request.POST["redirect_bad_url"] + "?formstate=" + json.dumps({"values" : values, "errors" : errors}))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + json.dumps({"values" : [], "errors" : ["showid"]}))
	except:
		return redirect("/")