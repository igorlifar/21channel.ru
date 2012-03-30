from news.models import *
from utils.views import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response

# Create your views here.

def create_news_item(request):
	try:
		values = []
		errors = []
		data = {}
		evaluate_char_field(request, "title", 1000, data, values, errors)
		evaluate_char_field(request, "preview", 1000, data, values, errors)
		evaluate_char_field(request, "text", 10000, data, values, errors)
		if len(data) == 3:
			newItem = NewsItem.objects.create(title = data["title"], preview = data["preview"], text = data["text"])
			newItem.save()
			if "image" in request.FILES:
				newItem.load_image(request.FILES["image"])
			return redirect(request.POST["redirect_good_url"])
		else:
			return redirect(request.POST["redirect_bad_url"] + "?formstate=" + json.dumps({"values" : values, "errors" : errors}))
	except:
		return redirect("/")

def delete_news_item(request):
	try:
		if "newsid" in request.POST:
			newsid = int(request.POST["newsid"])
			items = NewsItem.objects.filter(id = newsid)
			if items.count() != 0:
				item = items[0]
				if item.image.__nonzero__():
					item.image.delete()
				item.delete()
		return redirect(request.POST["redirect_url"])
	except:
		return redirect("/")
		
def update_news_item(request):
	try:
		if "newsid" in request.POST:
			newsid = int(request.POST["newsid"])
			items = NewsItem.objects.filter(id = newsid)
			if items.count() != 0:
				item = items[0]
				values = []
				errors = []
				data = {}
				evaluate_char_field(request, "title", 1000, data, values, errors)
				evaluate_char_field(request, "preview", 1000, data, values, errors)
				evaluate_char_field(request, "text", 10000, data, values, errors)
				if len(data) == 3:
					item.title = data["title"]
					item.preview = data["preview"]
					item.text = data["text"]
					item.save()
					if "image" in request.FILES:
						item.load_image(request.FILES["image"])
					return redirect(request.POST["redirect_good_url"])
				return redirect(request.POST["redirect_bad_url"] + "?formstate=" + json.dumps({"values" : values, "errors" : errors}))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + json.dumps({"values" : [], "errors" : ["newsid"]}))
	except:
		return redirect("/")