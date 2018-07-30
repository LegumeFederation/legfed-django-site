from cms.app_base import CMSApp
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.apphook_pool import apphook_pool

from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _

from polls_cms_integration.models import PollPluginModel

@apphook_pool.register  # register the application
class PollsApphook(CMSApp):
    app_name = "polls"
    name = _("Polls Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["polls.urls"]
