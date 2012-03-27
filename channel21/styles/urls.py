from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('styles',
        url(r'^site.css$', 'site.index'),
)