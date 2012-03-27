from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.http import HttpResponse

def convert_section(lst):
	res = {
		"size": 0,
		"levels": {}
	}
	
	i = 0
	for token in lst:
		res["size"] += 1
		res["levels"]["level" + str(i)] = token
		i += 1
		
	return res
	
def render_js_to_response(template, context):
	t = loader.get_template(template)
	c = Context(context)
	return HttpResponse(t.render(c), mimetype="text/javascript; charset=utf-8")
	
def render_panel(section, context, request):
	
	context.update({'section': convert_section(section)})
	context.update(csrf(request))
	
	return render_js_to_response('panel.js', context)
	
def render_site(section, context, request):
	
	context.update({'section': convert_section(section)})
	context.update(csrf(request))
	
	return render_js_to_response('site.js', context)