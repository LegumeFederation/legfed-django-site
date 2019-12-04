# -*- coding: utf-8 -*-
  
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from jobs_cms_integration.models import JobsPluginModel
from django.utils.translation import ugettext as _

@plugin_pool.register_plugin  # register the plugin
class JobsPluginPublisher(CMSPluginBase):
    model = JobsPluginModel  # model where plugin data are saved
    module = _("Jobs")
    name = _("Jobs Plugin")  # name of the plugin in the interface
    render_template = "jobs_cms_integration/jobs_plugin.html"

    def render(self, context, instance, placeholder):
        context.update({
            'open_jobs_list': self.model.get_jobs
        })
        return context

