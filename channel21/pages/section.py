from django.http import Http404
from news.models import NewsItem
from episodes.models import Episode
from shows.models import Show, Article, MetaItem, Shot
from archive.models import Archive
from schedule.models import Program
from mainsettings.models import MainSettings
from staticpages.models import Category, Page
from geolocation.models import geoLocation

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
				
			if path[2] == 'edit-local':
				return ['settings', 'edit-local']
		
		if path[1] == 'news':
		
			if len(path) == 2 or path[2] == 'list':
				return ['news', 'list']
			
			if path[2] == 'add':
				return ['news', 'add']
				
			if path[2] == 'edit':
				if len(path) == 3 or NewsItem.objects.filter(id=path[3]).count() == 0:
					raise Http404
				
				return ['news', 'edit', path[3]]
				
			if path[2] == 'delete-check':
				return ['news', 'delete-check']
				
		
		if path[1] == 'shows':
			if len(path) == 2 or path[2] == 'list':
				return ['shows', 'list']
			
			if path[2] == 'add':
				return ['shows', 'add']
				
			if path[2] == 'edit':
				if len(path) == 3 or Show.objects.filter(id = path[3]).count() == 0:
					raise Http404
				
				return ['shows', 'edit', path[3]]
		
			if path[2] == 'delete-check':
				return ['shows', 'delete-check']
		
			if path[2] == 'list-shots':
				if len(path) == 3 or Show.objects.filter(id = path[3]).count() == 0:
					raise Http404
				
				return ['shows', 'list-shots', path[3]]
		
			if path[2] == 'add-shot':
				if len(path) == 3 or Show.objects.filter(id = path[3]).count() == 0:
					raise Http404
				
				return ["shows", "add-shot", path[3]]
				
			if path[2] == "edit-shot":
				if len(path) == 3 or Shot.objects.filter(id = path[3]).count() == 0:
					raise Http404
				
				return ["shows", "edit-shot", path[3]]
				
			if path[2] == "delete-shot":
				return ["shows", "delete-shot"]
				
			if path[2] == "list-articles":
				if len(path) == 3 or Show.objects.filter(id = path[3]).count() == 0:
					raise Http404
				
				return ["shows", "list-articles", path[3]]
				
			if path[2] == "edit-article":
				if len(path) == 3 or Article.objects.filter(id = path[3]).count() == 0:
					raise Http404
				
				return ["shows", "edit-article", path[3]]
				
			if path[2] == "add-article":
				if len(path) == 3 or Show.objects.filter(id = path[3]).count() == 0:
					raise Http404
				
				return ["shows", "add-article", path[3]]
		
			if path[2] == "delete-article":
				return ["shows", "delete-article"]
		
			if path[2] == "list-meta":
				if len(path) == 3 or Show.objects.filter(id = path[3]).count() == 0:
					raise Http404
				
				return ["shows", "list-meta", path[3]]
		
			if path[2] == "add-meta":
				if len(path) == 3 or Show.objects.filter(id = path[3]).count() == 0:
					raise Http404
				
				return ["shows", "add-meta", path[3]]
		
			if path[2] == "edit-meta":
				if len(path) == 3 or MetaItem.objects.filter(id = path[3]).count() == 0:
					raise Http404
				
				return ["shows", "edit-meta", path[3]]
		
			if path[2] == "delete-meta":
				return ["shows", "delete-meta"]
		
		if path[1] == 'archive':
			if len(path) == 2 or path[2] == 'list':
				return ['archive', 'list']
			
			if path[2] == 'add':
				return ['archive', 'add']
				
			if path[2] == 'edit':
				if len(path) == 3 or Archive.objects.filter(id = path[3]).count() == 0:
					raise Http404
				
				return ['archive', 'edit', path[3]]
				
			if path[2] == 'delete-check':
				return ['archive', 'delete-check']
		
		if path[1] == 'episodes':
			if len(path) == 2 or path[2] == 'list':
				return ['episodes', 'list']
			
			if path[2] == 'add':
				return ['episodes', 'add']
		
			if path[2] == 'edit':
				if len(path) == 3 or Episode.objects.filter(id = path[3]).count() == 0:
					raise Http404
				
				return ['episodes', 'edit', path[3]]
		
			if path[2] == 'delete-check':
				return ['episodes', 'delete-check']
		
		if path[1] == 'schedule':
			if len(path) == 2 or path[2] == 'list':
				return ["schedule", 'list']
				
			if path[2] == 'add':
				return ['schedule', 'add']
				
			if path[2] == 'edit':
				if len(path) == 3:
					raise Http404
				
				programs = Program.objects.filter(id = path[3])
				if programs.count() == 0 or programs[0].region != None:
					raise Http404
				
				return ['schedule', 'edit', path[3]]
			
			if path[2] == 'delete-check':
				return ['schedule', 'delete-check']

			if path[2] == 'local':
				return ['schedule', 'local']
				
			if path[2] == 'local-add':
				return ['schedule', 'local-add']
				
			if path[2] == 'local-edit':
				if len(path) == 3:
					raise Http404
				
				programs = Program.objects.filter(id = path[3])
				if programs.count() == 0 or programs[0].region == None:
					raise Http404
				
				return ['schedule', 'local-edit', path[3]]
				
		if path[1] == 'pages':
			if len(path) == 2 or path[2] == 'list':
				return ['pages', 'list']

			if path[2] == 'add':
				return ['pages', 'add']

			if path[2] == 'edit' and Page.objects.filter(id = path[3]).count() != 0:
				return ['pages', 'edit', path[3]]
				
			if path[2] == 'delete-check':
				return ['pages', 'delete-check']
		
		if path[1] == 'regions':
			if len(path) == 2 or path[2] == 'list':
				return ['regions', 'list']
			
			if path[2] == 'add':
				return ['regions', 'add']
				
			if path[2] == 'delete-check':
				return ['regions', 'delete-check']
				
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
			
		if len(path) == 5 and path[2] == 'promo' and path[3] == 'watch':
			try:
				vd = Episode.objects.get(show=sh, id=int(path[4]), episodetype='P')
				return ["shows", path[1], "promo", "watch", path[4]]
			except:
				raise Http404
			
		if path[2] == 'issues':
			if len(path) == 3:
				return ['shows', path[1], 'issues']
				
			if len(path) == 5 and path[3] == 'watch':
				try:
					vd = Episode.objects.get(show=sh, id=int(path[4]), episodetype="I")
					return ["shows", path[1], "issues", "watch", path[4]]
				except:
					raise Http404
		
		if path[2] == 'episodes':
			if len(path) == 3:
				return ['shows', path[1], 'episodes']
				
			if len(path) == 5 and path[3] == 'watch':
				try:
					vd = Episode.objects.get(show=sh, id=int(path[4]), episodetype="E")
					return ["shows", path[1], "episodes", "watch", path[4]]
				except:
					raise Http404
		
		
		if path[2] == 'watch':
			ep = None
			try:
				ep = Episode.objects.get(show=sh, id=int(path[3]))
			except:
				raise Http404
			
			return ['shows', path[1], 'watch', path[3]]

	if path[0] == 'pages':
		try:
			page = Page.objects.get(id=path[1])
		except:
			raise Http404

		return ['pages', path[1]]
		
		
	raise Http404
