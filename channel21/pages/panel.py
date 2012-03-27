from django.http import HttpResponse, Http404
from django.shortcuts import redirect

from pages.section import get_panel_section
from pages.context import get_panel_context
from pages.shortcuts import render_panel

def index(request):
	
	if not request.user.is_superuser:
		return redirect("/panel/login-page/")
	
	section = get_panel_section(request)
	context = get_panel_context(section, request)
	
	return render_panel(section, context, request)