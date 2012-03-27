from django.http import HttpResponse, Http404

from styles.section import get_panel_section
from styles.context import get_panel_context
from styles.shortcuts import render_panel

def index(request):
	section = get_panel_section(request)
	context = get_panel_context(section, request)
	
	return render_panel(section, context, request)