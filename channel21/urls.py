from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^styles/', include('styles.urls')),
    url(r'^scripts/', include('scripts.urls')),
    url(r'^static_files/(?P<path>.*)$',  'django.views.static.serve', {'document_root': '/home/gasya/Documents/21channel.ru/static/' }),
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'', include('pages.urls')),
)
