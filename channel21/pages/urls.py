from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('pages',
	url(r'^panel/$', 'panel.index'),
	url(r'^panel/login/$', 'panel.index'),
	url(r'^panel/news/', 'panel.index'),
	url(r'^panel/shows/', 'panel.index'),
	url(r'^panel/archive/', 'panel.index'),
	url(r'^panel/episodes/', 'panel.index'),
	url(r'^panel/schedule/', 'panel.index'),
	url(r'^panel/settings/', 'panel.index'),
	
	url(r'^$', 'site.index'),
	url(r'^shows/', 'site.index'),
	url(r'^news/', 'site.index'),
	url(r'^archive/', 'site.index'),
	url(r'^episode/', 'site.index'),
	url(r'^schedule/', 'site.index'),
	url(r'^coverage/', 'site.index'),
)