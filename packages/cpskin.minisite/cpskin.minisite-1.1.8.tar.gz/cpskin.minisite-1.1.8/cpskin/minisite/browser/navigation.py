# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from cpskin.minisite.utils import get_minisite_path
from Products.CMFPlone import utils
from Products.CMFPlone.browser.interfaces import INavigationBreadcrumbs
from Products.CMFPlone.browser.navigation import get_view_url
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs
from Products.Five import BrowserView
from zope.component import getMultiAdapter
from zope.interface import implements


class MinisiteNavigationBreadcrumbs(BrowserView):
    implements(INavigationBreadcrumbs)

    def breadcrumbs(self):
        context = aq_inner(self.context)
        request = self.request
        container = utils.parent(context)

        name, item_url = get_view_url(context)

        if container is None:
            return ({'absolute_url': item_url,
                     'Title': utils.pretty_title_or_id(context, context), },
                    )

        view = getMultiAdapter((container, request), name='breadcrumbs_view')
        base = tuple(view.breadcrumbs())

        # Some things want to be hidden from the breadcrumbs
        if IHideFromBreadcrumbs.providedBy(context):
            return base

        if base:
            item_url = '%s/%s' % (base[-1]['absolute_url'], name)

        # only next line change from
        # Products.CMFPlone.browser.navigation.PhysicalNavigationBreadcrumbs
        rootPath = get_minisite_path(request)
        itemPath = '/'.join(context.getPhysicalPath())

        # don't show default pages in breadcrumbs or pages above the navigation
        # root
        if not utils.isDefaultPage(context, request) \
                and not rootPath.startswith(itemPath):
            base += ({'absolute_url': item_url,
                      'Title': utils.pretty_title_or_id(context, context), },
                     )

        return base
