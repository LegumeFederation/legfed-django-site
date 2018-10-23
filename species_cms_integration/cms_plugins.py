# -*- coding: utf-8 -*-

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from species_cms_integration.models import SpeciesPluginModel
from django.utils.translation import ugettext as _

@plugin_pool.register_plugin  # register the plugin
class SpeciesPluginPublisher(CMSPluginBase):
    model = SpeciesPluginModel  # model where plugin data are saved
    module = _("Species")
    name = _("Species Plugin")  # name of the plugin in the interface
    render_template = "species_cms_integration/species_plugin.html"

    def render(self, context, instance, placeholder):
        context.update({
            'latest_species_and_urls_list': self.model.get_species_with_resources
        })
        return context

