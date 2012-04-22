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
				values = {}
				errors = {}
				if "priority" in request.POST:
					try:
						values["priority"] = int(request.POST["priority"])
						errors["priority"] = False
					except:
						values["priority"] = ""
						errors["priority"] = True
				else:
					values["priority"] = ""
					errors["priority"] = True
				if not errors["priority"]:
					new_shot = Shot.objects.create(priority = values["priority"], show = cshow)
					if "shot" in request.FILES:
						try:
							new_shot.load_shot(request.FILES["shot"])
							errors["shot"] = False
						except:
							new_shot.delete()
							errors["shot"] = True
					else:
						new_shot.delete()
						errors["shot"] = True
				if not errors["priority"] and not errors["shot"]:
					return redirect(request.POST["redirect_good_url"])
				return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : {}, "errors" : {"showid" : True}})))
	except:
		return redirect("/")
		
def update_shot(request):
	try:
		if "shotid" in request.POST:
			shotid = int(request.POST["shotid"])
			shots = Shot.objects.filter(id = shotid)
			if shots.count() != 0:
				shot = shots[0]
				if "priority" in request.POST:
					try:
						npriority = int(request.POST["priority"])
						shot.priority = npriority
						shot.save()
						return redirect(request.POST["redirect_good_url"])
					except:
						return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : {}, "errors" : {"priority" : True}})))
				return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : {}, "errors" : {"priority" : True}})))
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
				if shot.shot_small.__nonzero__():
					shot.shot_small.delete()
				if shot.shot_big.__nonzero__():
					shot.shot_big.delete()
				shot.delete()
		return redirect(request.POST["redirect_url"])
	except:
		return redirect("/")
		
def create_meta_item(request):
	try:
		if "showid" in request.POST:
			showid = int(request.POST["showid"])
			shows = Show.objects.filter(id = showid)
			if shows.count() != 0:
				cshow = shows[0]
				values = {}
				errors = {}
				data = {}
				evaluate_char_field(request, "key", 100, data, values, errors)
				evaluate_char_field(request, "value", 1000, data, values, errors)
				if "priority" in request.POST:
					try:
						data["priority"] = int(request.POST["priority"])
						values["priority"] = data["priority"]
						errors["priority"] = False
					except:
						values["priority"] = ""
						errors["priority"] = True
				else:
					values["priority"] = ""
					errors["priority"] = True
				if len(data) == 3:
					new_meta_item = MetaItem.objects.create(key = data["key"], value = data["value"], priority = data["priority"], show = cshow)
					return redirect(request.POST["redirect_good_url"])
				return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : {}, "errors" : {"showid" : True}})))
	except:
		return redirect("/")
		
def update_meta_item(request):
	try:
		if "metaitemid" in request.POST:
			metaitemid = int(request.POST["metaitemid"])
			metaitems = MetaItem.objects.filter(id = metaitemid)
			if metaitems.count() != 0:
				metaitem = metaitems[0]
				values = {}
				errors = {}
				data = {}
				evaluate_char_field(request, "key", 100, data, values, errors)
				evaluate_char_field(request, "value", 1000, data, values, errors)
				if "priority" in request.POST:
					try:
						data["priority"] = int(request.POST["priority"])
						values["priority"] = data["priority"]
						errors["priority"] = False
					except:
						values["priority"] = ""
						errors["priority"] = True
				else:
					values["priority"] = ""
					errors["priority"] = True
				if len(data) == 3:
					metaitem.key = data["key"]
					metaitem.value = data["value"]
					metaitem.priority = data["priority"]
					metaitem.save()
					return redirect(request.POST["redirect_good_url"])
				return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : {}, "errors" : {"metaitemid" : True}})))
	except:
		return redirect("/")
		
def delete_meta_item(request):
	try:
		if "metaitemid" in request.POST:
			metaitemid = int(request.POST["metaitemid"])
			metaitems = MetaItem.objects.filter(id = metaitemid)
			if metaitems.count() != 0:
				metaitem = metaitems[0]
				metaitem.delete()
		return redirect(request.POST["redirect_url"])
	except:
		return redirect("/")
		
def create_article(request):
	try:
		if "showid" in request.POST:
			showid = int(request.POST["showid"])
			shows = Show.objects.filter(id = showid)
			if shows.count() != 0:
				cshow = shows[0]
				values = {}
				errors = {}
				data = {}
				values["articletype"] = ""
				errors["articletype"] = True
				if "articletype" in request.POST:
					articletype = request.POST["articletype"]
					if articletype == "Article":
						data["articletype"] = "A"
						values["articletype"] = "Article"
						errors["articletype"] = False
					if articletype == "Review":
						data["articletype"] = "R"
						values["articletype"] = "Review"
						errors["articletype"] = False
				evaluate_char_field(request, "title", 1000, data, values, errors)
				evaluate_char_field(request, "preview", 1000, data, values, errors)
				evaluate_char_field(request, "text", 10000, data, values, errors)
				evaluate_char_field(request, "author", 1000, data, values, errors)
				if "priority" in request.POST:
					try:
						data["priority"] = int(request.POST["priority"])
						values["priority"] = data["priority"]
						errors["priority"] = False
					except:
						values["priority"] = ""
						errors["priority"] = True
				else:
					values["priority"] = ""
					errors["priority"] = True
				if len(data) == 6:
					new_article = Article.objects.create(articletype = data["articletype"], title = data["title"], preview = data["preview"], text = data["text"], author = data["author"], priority = data["priority"], show = cshow)
					return redirect(request.POST["redirect_good_url"])
				return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : {}, "errors" : {"showid" : True}})))
	except:
		return redirect("/")
		
def update_article(request):
	try:
		if "articleid" in request.POST:
			articleid = int(request.POST["articleid"])
			articles = Article.objects.filter(id = articleid)
			if articles.count() != 0:
				article = articles[0]
				values = {}
				errors = {}
				data = {}
				values["articletype"] = ""
				errors["articletype"] = True
				if "articletype" in request.POST:
					articletype = request.POST["articletype"]
					if articletype == "Article":
						data["articletype"] = "A"
						values["articletype"] = "Article"
						errors["articletype"] = False
					if articletype == "Review":
						data["articletype"] = "R"
						values["articletype"] = "Review"
						errors["articletype"] = False
				evaluate_char_field(request, "title", 1000, data, values, errors)
				evaluate_char_field(request, "preview", 1000, data, values, errors)
				evaluate_char_field(request, "text", 10000, data, values, errors)
				evaluate_char_field(request, "author", 1000, data, values, errors)
				if "priority" in request.POST:
					try:
						data["priority"] = int(request.POST["priority"])
						values["priority"] = data["priority"]
						errors["priority"] = False
					except:
						values["priority"] = ""
						errors["priority"] = True
				else:
					values["priority"] = ""
					errors["priority"] = True
				if len(data) == 6:
					article.articletype = data["articletype"]
					article.title = data["title"]
					article.preview = data["preview"]
					article.text = data["text"]
					article.author = data["author"]
					article.priority = data["priority"]
					article.save()
					return redirect(request.POST["redirect_good_url"])
				return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : {}, "errors" : {"articleid" : True}})))
	except:
		return redirect("/")
		
def delete_article(request):
	try:
		if "articleid" in request.POST:
			articleid = int(request.POST["articleid"])
			articles = Article.objects.filter(id = articleid)
			if articles.count() != 0:
				article = articles[0]
				article.delete()
		return redirect(request.POST["redirect_url"])
	except:
		return redirect("/")