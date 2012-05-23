from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import Context, loader

from profiling import profile

def convert_section(lst):
	res = {
		"size": 0,
	}
	
	i = 0
	for token in lst:
		res["size"] += 1
		res[str(i)] = token
		i += 1
		
	return res
	
def render_panel(section, context, request):
	
	context.update({'s': convert_section(section)})
	context.update(csrf(request))
	
	return render_to_response('panel.html', context)
	
@profile('render_site.prof')
def render_site(section, context, request):
	
	context.update({'s': convert_section(section)})
	context.update({'media': '/media_files/'})
	context.update({'static': '/static_files/'})
	context.update({'img': '/static_files/img/'})
	
	context.update(csrf(request))
	
	return render_to_response('site.html', context)