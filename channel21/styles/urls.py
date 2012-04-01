from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('styles',
	url(r'^site.css$', 'site.index'),
	url(r'^archive-list.css$', 'site.index'),
	url(r'^archive-category.css$', 'site.index'),
	url(r'^episode.css$', 'site.index'),
	url(r'^schedule.css$', 'site.index'),
	url(r'^coverage.css$', 'site.index'),
	url(r'^news-list.css$', 'site.index'),
	url(r'^news-item.css$', 'site.index'),
	url(r'^shows-list.css$', 'site.index'),
	url(r'^shows-show.css$', 'site.index'),
	url(r'^shows-show-episode.css$', 'site.index'),
	url(r'^shows-banner.css', 'site.index'),
)