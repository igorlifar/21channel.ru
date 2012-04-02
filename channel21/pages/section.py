from django.http import Http404
from news.models import NewsItem
from episodes.models import Episode
from shows.models import Show
from archive.models import Archive
from schedule.models import Program
from mainsettings.models import MainSettings

def get_panel_section(request):
	path = request.path.strip('/').split('/')
	
	if len(path) > 0 and path[0] == 'panel':
		if len(path) == 1:
			return ['index']
		
		if path[1] == 'login':
			return ['login']
		
		if path[1] == 'settings':
			if len(path) == 2 or path[2] == 'list':
				return ['settings', 'list']
				
			if path[2] == 'edit':
				return ['settings', 'edit']
		
		if path[1] == 'news':
			if len(path) == 2 or path[2] == 'list':
				return ['news', 'list']
			
			if path[2] == 'add':
				return ['news', 'add']
				
			if path[2] == 'edit':
				if len(path) == 3 or NewsItem.objects.filter(id=path[3]).count() == 0:
					raise Http404
				
				return ['news', 'edit', path[3]]
				
		
		if path[1] == 'shows':
			if len(path) == 2 or path[2] == 'list':
				return ['shows', 'list']
			
			if path[2] == 'add':
				return ['shows', 'add']
				
			if path[2] == 'edit':
				if len(path) == 3 or Show.objects.filter(id = path[3]).count() == 0:
					raise Http404
				
				return ['shows', 'edit', path[3]]
		
		if path[1] == 'archive':
			if len(path) == 2 or path[2] == 'list':
				return ['archive', 'list']
			
			if path[2] == 'add':
				return ['archive', 'add']
				
			if path[2] == 'edit':
				if len(path) == 3 or Archive.objects.filter(id = path[3]).count() == 0:
					raise Http404
				
				return ['archive', 'edit', path[3]]
		
		if path[1] == 'episodes':
			if len(path) == 2 or path[2] == 'list':
				return ['episodes', 'list']
			
			if path[2] == 'add':
				return ['episodes', 'add']
		
			if path[2] == 'edit':
				if len(path) == 3 or Episode.objects.filter(id = path[3]).count() == 0:
					raise Http404
				
				return ['episodes', 'edit', path[3]]
		
		if path[1] == 'schedule':
			if len(path) == 2 or path[2] == 'list':
				return ["schedule", 'list']
				
			if path[2] == 'add':
				return ['schedule', 'add']
				
			if path[2] == 'edit':
				if len(path) == 3 or Program.objects.filter(id = path[3]).count() == 0:
					raise Http404
				
				return ['schedule', 'edit', path[3]]
			
		
	raise Http404
	
def get_site_section(request):
	path = []
	
	if request.path != '/':
		path = request.path.strip('/').split('/')
	else:
		path = ['index']
	
		
	if path[0] == "index":
		if len(path) == 1:
			return ["index"]
			
	if path[0] == 'archive':
		if len(path) == 1:
			return ['archive', 'list']
			
		if len(path) == 2:
			try:
				cat = Archive.objects.get(id=int(path[1]))
				return ['archive', path[1]]
			except:
				raise Http404

			
	if len(path) == 2 and path[0] == 'episode':
		try:
			ep = Episode.objects.get(id=int(path[1]))
			return ['episode', path[1]]
		except:
			raise Http404
		
	if len(path) == 1 and path[0] == 'schedule':
		return ['schedule']
		
	if len(path) == 1 and path[0] == 'coverage':
		return ['coverage']
	
	if path[0] == 'news':
		if len(path) == 1:
			return ['news', 'list']
			
		try:
			ns = NewsItem.objects.get(id=int(path[1]))
			return ['news', path[1]]
		except:
			raise Http404
	
	
	if path[0] == 'shows':
		if len(path) == 1:
			return ["shows", "list"]
		
		sh = None
		try:
			sh = Show.objects.get(id=int(path[1]))
		except:
			raise Http404
		
		if len(path) == 2:
			return ["shows", path[1]]
			
		if path[2] == 'episode':
			ep = None
			try:
				ep = Episode.objects.get(show=sh, id=int(path[3]))
			except:
				raise Http404
			
			return ['shows', path[1], 'episode', path[3]]
		
		
	raise Http404
