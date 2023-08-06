# -*- coding: utf-8 -*-
from cpskin.locales import CPSkinMessageFactory as _
from cpskin.minisite.browser.interfaces import IHNavigationActivated
from cpskin.minisite.browser.interfaces import IHNavigationActivationView
from cpskin.minisite.utils import get_minisite_object
from cpskin.minisite.utils import list_minisites
from plone import api
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import noLongerProvides


class MSHorizontalNavigation(BrowserView):
    implements(IHNavigationActivationView)
    """
    Horizontal navigation activation helper view
    """

    @property
    def is_in_minisite_mode(self):
        portal = api.portal.get()
        minisites = list_minisites(portal)
        for minisite in minisites:
            if "/".join(self.context.getPhysicalPath()).startswith(minisite.search_path):
                return True
        return False
        # import ipdb; ipdb.set_trace()
        #
        # minisite = self.request.get('cpskin_minisite', None)
        # if not isinstance(minisite, Minisite):
        #     return
        # if minisite.is_in_minisite_mode:
        #     return True
        # else:
        #     return False

    @property
    def can_enable_hnavigation(self):
        minisite_root = get_minisite_object(self.request)
        return self.is_in_minisite_mode and not (IHNavigationActivated.providedBy(minisite_root))

    @property
    def can_disable_hnavigation(self):
        minisite_root = get_minisite_object(self.request)
        return self.is_in_minisite_mode and (IHNavigationActivated.providedBy(minisite_root))


def _redirect(self, msg=''):
    if self.request:
        if msg:
            api.portal.show_message(message=msg,
                                    request=self.request,
                                    type='info')

        self.request.response.redirect(self.context.absolute_url())
    return msg


class MSHorizontalNavigationEnable(BrowserView):
    """
    Horizontal navigation activation helper view
    """

    def __init__(self, context, request):
        super(MSHorizontalNavigationEnable, self).__init__(context, request)
        alsoProvides(get_minisite_object(request), IHNavigationActivated)
        _redirect(self, msg=_(u'Minisite horizontal Navigation enabled on content'))


class MSHorizontalNavigationDisable(BrowserView):
    """
    Horizontal navigation activation helper view
    """

    def __init__(self, context, request):
        super(MSHorizontalNavigationDisable, self).__init__(context, request)
        noLongerProvides(get_minisite_object(request), IHNavigationActivated)
        _redirect(self, msg=_(u'Minisite horizontal Navigation disabled on content'))
