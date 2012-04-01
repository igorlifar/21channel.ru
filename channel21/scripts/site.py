from django.http import HttpResponse, Http404

from scripts.section import get_site_section
from scripts.context import get_site_context
from scripts.shortcuts import render_site

def index(request):
	section = get_site_section(request)
	context = get_site_context(section, request)
	
	return render_site(section, context, request)