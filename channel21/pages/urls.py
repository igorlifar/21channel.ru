from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('pages',
	url(r'^panel/$', 'panel.index'),
	url(r'^panel/login/$', 'panel.index'),
	url(r'^panel/news/', 'panel.index'),
	url(r'^panel/shows/', 'panel.index'),
	url(r'^panel/archive/', 'panel.index'),
	url(r'^panel/episodes/', 'panel.index'),
)