from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^panel/login/send', 'profiles.views.login_panel'),
	url(r'^panel/logout/', 'profiles.views.logout_panel'),
	
	url(r'^panel/news/delete/$', 'news.views.delete_news_item'),
	url(r'^panel/news/edit/send/$', 'news.views.update_news_item'),
	url(r'^panel/news/add/send/$', 'news.views.create_news_item'),
	
	url(r'^panel/episodes/delete/$', 'episodes.views.delete_episode'),
	url(r'^panel/episodes/edit/send/$', 'episodes.views.update_episode'),
	
	url(r'^panel/shows/delete/$', 'shows.views.delete_show'),
	url(r'^panel/shows/edit/send/$', 'shows.views.update_show'),
	
	url(r'^panel/archive/delete/$', 'archive.views.delete_archive'),
	
	url(r'^styles/', include('styles.urls')),
	url(r'^scripts/', include('scripts.urls')),
    
	url(r'^static_files/(?P<path>.*)$',  'django.views.static.serve', {'document_root': '/home/gasya/Documents/21channel.ru/static/' }),
	url(r'^media_files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/gasya/Documents/21channel.ru/media/' }),
    
	url(r'^django-admin/', include(admin.site.urls)),
	url(r'', include('pages.urls')),
)
