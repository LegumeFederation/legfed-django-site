# -*- coding: utf-8 -*-

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from resources_cms_integration.models import DataDownloadsPluginModel, ToursPluginModel, ToolsPluginModel
from django.utils.translation import ugettext as _

@plugin_pool.register_plugin  # register the plugin
class DataDownloadsPluginPublisher(CMSPluginBase):
    model = DataDownloadsPluginModel  # model where plugin data are saved
    module = _("Data Downloads")
    name = _("Data Downloads Plugin")  # name of the plugin in the interface
    render_template = "resources_cms_integration/data_downloads_plugin.html"

    def render(self, context, instance, placeholder):
        context.update({
            'data_downloads_list': self.model.get_data_downloads
        })
        return context

@plugin_pool.register_plugin  # register the plugin
class ToursPluginPublisher(CMSPluginBase):
    model = ToursPluginModel  # model where plugin data are saved
    module = _("Tours")
    name = _("Tours Plugin")  # name of the plugin in the interface
    render_template = "resources_cms_integration/tours_plugin.html"

    def render(self, context, instance, placeholder):
        context.update({
            'tours_list': self.model.get_tours
        })
        return context

@plugin_pool.register_plugin  # register the plugin
class ToolsPluginPublisher(CMSPluginBase):
    model = ToolsPluginModel  # model where plugin data are saved
    module = _("Tools")
    name = _("Tools Plugin")  # name of the plugin in the interface
    render_template = "resources_cms_integration/tools_plugin.html"

    def render(self, context, instance, placeholder):
        context.update({
            'tools_list': self.model.get_tools
        })
        return context

