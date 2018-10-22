# -*- coding: utf-8 -*-

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from announcements_cms_integration.models import AnnouncementPluginModel
from django.utils.translation import ugettext as _

@plugin_pool.register_plugin  # register the plugin
class AnnouncementPluginPublisher(CMSPluginBase):
    model = AnnouncementPluginModel  # model where plugin data are saved
    module = _("Announcements")
    name = _("Announcement Plugin")  # name of the plugin in the interface
    render_template = "announcements_cms_integration/announcement_plugin.html"

    def render(self, context, instance, placeholder):
        context.update({
            'latest_announcements_list': self.model.get_announcements
        })
        return context

