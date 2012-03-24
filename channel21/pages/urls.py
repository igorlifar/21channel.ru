from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('pages',
        url(r'^panel/$', 'panel.index'),
)