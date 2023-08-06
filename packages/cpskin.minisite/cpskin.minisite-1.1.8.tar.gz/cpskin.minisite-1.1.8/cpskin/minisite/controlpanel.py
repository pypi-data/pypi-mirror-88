from zope.component import getUtilitiesFor
from Products.Five.browser import BrowserView

from cpskin.minisite.interfaces import IMinisiteConfig


class MinisitesPanel(BrowserView):

    def minisites(self):
        portal_path = '/'.join(self.context.getPhysicalPath())
        configs = getUtilitiesFor(IMinisiteConfig, self.context)
        result = [
            config for name, config in configs
            if config.search_path.startswith(portal_path)
        ]
        return result
