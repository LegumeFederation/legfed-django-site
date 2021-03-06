# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

admin.autodiscover()

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'cmspages': CMSSitemap}}),
]

urlpatterns += i18n_patterns(
    url(r'^polls/', include('polls.urls')),
    url(r'^species_mgr/', include('species_mgr.urls')),
    url(r'^resource_mgr/', include('resource_mgr.urls')),
    url(r'^announcements/', include('announcements.urls')),
    url(r'^linkout_mgr/', include('linkout_mgr.urls')),
    url(r'^intermine_mgr/', include('intermine_mgr.urls')),
    url(r'^jobs/', include('jobs.urls')),
    url(r'^admin/', include(admin.site.urls)),  # NOQA
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^plugin_forms/', include('cmsplugin_form_handler.urls', namespace='cmsplugin_form_handler')),
    url(r'^', include('djangocms_forms.urls')),
    url(r'^', include('cms.urls')),
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ] + staticfiles_urlpatterns() + urlpatterns

