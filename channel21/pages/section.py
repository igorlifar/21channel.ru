from django.http import Http404
from news.models import NewsItem

def get_panel_section(request):
	path = request.path.strip('/').split('/')
	
	if len(path) > 0 and path[0] == 'panel':
		if len(path) == 1:
			return ['index']
		
		if path[1] == 'login':
			return ['login']
		
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
				
		
		if path[1] == 'archive':
			if len(path) == 2 or path[2] == 'list':
				return ['archive', 'list']
			
			if path[2] == 'add':
				return ['archive', 'add']
				
		
		if path[1] == 'episodes':
			if len(path) == 2 or path[2] == 'list':
				return ['episodes', 'list']
			
			if path[2] == 'add':
				return ['episodes', 'add']
		
				
		
				
			
		
	raise Http404
	
def get_site_section(request):
	path = request.path.strip('/').split('/')
	
	level1 = ["shows", "archive", "episode", "schedule"]
	
	if len(path) == 0 or not path[0] in a:
		path.insert(0, "index")
		
	if path[0] == "index":
		if len(path) == 1:
			return ["index"]
		else:
			raise Http404
	else:
		raise Http404