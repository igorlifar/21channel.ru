from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('scripts',
	url(r'^site.js$', 'site.index'),
	url(r'^archive-list.js$', 'site.index'),
	url(r'^archive-category.js$', 'site.index'),
	url(r'^episode.js$', 'site.index'),
	url(r'^schedule.js$', 'site.index'),
	url(r'^coverage.js$', 'site.index'),
	url(r'^news-list.js$', 'site.index'),
	url(r'^news-item.js$', 'site.index'),
	url(r'^shows-list.js$', 'site.index'),
	url(r'^shows-show.js$', 'site.index'),
	url(r'^shows-show-watch.js$', 'site.index'),
	url(r'^shows-show-issues.js$', 'site.index'),
	url(r'^shows-show-episodes.js$', 'site.index'),
)