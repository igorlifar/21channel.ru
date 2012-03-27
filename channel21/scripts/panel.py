from django.http import HttpResponse, Http404

from scripts.section import get_panel_section
from scripts.context import get_panel_context
from scripts.shortcuts import render_panel

def index(request):
	section = get_panel_section(request)
	context = get_panel_context(section, request)
	
	return render_panel(section, context, request)