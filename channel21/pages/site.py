from django.http import HttpResponse, Http404

from pages.section import get_site_section
from pages.context import get_site_context
from pages.shortcuts import render_site

def index(request):
	section = get_site_section(request)
	context = get_site_context(section, request)

	return render_site(section, context, request)
