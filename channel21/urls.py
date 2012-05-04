from django.conf.urls.defaults import patterns, include, url
from settings import rel

# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	url(r'^ulogin/', include('django_ulogin.urls')),
	
	url(r'^profiles/logout/$', 'profiles.views.logout_site'),
	
	url(r'^comments/show/create/$', 'comments.views.create_show_comment'),
	

	url(r'^panel/login/send', 'profiles.views.login_panel'),
	url(r'^panel/logout/', 'profiles.views.logout_panel'),
	
	url(r'^panel/settings/edit/send/$', 'mainsettings.views.update_settings'),
	
	url(r'^panel/news/delete/$', 'news.views.delete_news_item'),
	url(r'^panel/news/edit/send/$', 'news.views.update_news_item'),
	url(r'^panel/news/add/send/$', 'news.views.create_news_item'),
	
	url(r'^panel/episodes/delete/$', 'episodes.views.delete_episode'),
	url(r'^panel/episodes/edit/send/$', 'episodes.views.update_episode'),
	url(r'^panel/episodes/add/send/$', 'episodes.views.create_episode'),
	
	url(r'^panel/shows/delete/$', 'shows.views.delete_show'),
	url(r'^panel/shows/edit/send/$', 'shows.views.update_show'),
	url(r'^panel/shows/add/send/$', 'shows.views.create_show'),
	url(r'^panel/shows/add-shot/send/$', 'shows.views.create_shot'),
	url(r'^panel/shows/add-article/send/$', 'shows.views.create_article'),
	url(r'^panel/shows/delete-shot/send/$', 'shows.views.delete_shot'),
	url(r'^panel/shows/delete-article/send/$', 'shows.views.delete_article'),
	url(r'^panel/shows/add-meta/send/$', 'shows.views.create_meta_item'),
	url(r'^panel/shows/delete-meta/send/$', 'shows.views.delete_meta_item'),
	url(r'^panel/shows/edit-article/send/$', 'shows.views.update_article'),
	url(r'^panel/shows/edit-meta/send/$', 'shows.views.update_meta_item'),
	url(r'^panel/shows/edit-shot/send/$', 'shows.views.update_shot'),
	
	url(r'^panel/archive/delete/$', 'archive.views.delete_archive'),
	url(r'^panel/archive/edit/edit-archive/$', 'archive.views.update_archive'),
	url(r'^panel/archive/edit/delete-episode/$', 'archive.views.delete_episode_from_archive'),
	url(r'^panel/archive/edit/add-episode/$', 'archive.views.add_episode_to_archive'),
	url(r'^panel/archive/add/send/$', 'archive.views.create_archive'),
	
	url(r'^panel/schedule/add/send/$', 'schedule.views.create_program'),
	url(r'^panel/schedule/delete/$', 'schedule.views.delete_program'),
	url(r'^panel/schedule/edit/send/$', 'schedule.views.update_program'),
	
	url(r'^styles/', include('styles.urls')),
	url(r'^scripts/', include('scripts.urls')),
    
	url(r'^static_files/(?P<path>.*)$',  'django.views.static.serve', {'document_root': rel('static/') }),
	url(r'^media_files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': rel('media/') }),
    
	url(r'^django-admin/', include(admin.site.urls)),
	url(r'', include('pages.urls')),
)
