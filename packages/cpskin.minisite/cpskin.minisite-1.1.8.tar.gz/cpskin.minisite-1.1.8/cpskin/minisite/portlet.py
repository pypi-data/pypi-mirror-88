from Acquisition import aq_inner
from persistent.dict import PersistentDict
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.interface import implements
from plone import api
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager, \
                                      IPortletAssignmentMapping
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from cpskin.minisite.interfaces import IInMinisite
from cpskin.minisite.minisite import Minisite
from cpskin.minisite.viewlet import MinisiteViewlet


class IMiniSitePortlet(IPortletDataProvider):
    """
    Mini Site portlet interface
    """


class Assignment(base.Assignment):
    implements(IMiniSitePortlet)

    @property
    def title(self):
        return "Mini site"


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('portlet.pt')

    @property
    def available(self):
        request = self.request
        return IInMinisite.providedBy(request)

    def viewlet(self):
        context = self.context
        request = self.request
        context = aq_inner(context)
        viewlet = MinisiteViewlet(context, request, None, None).__of__(context)
        viewlet.update()
        return viewlet.render()


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()


def checkPortlet(request, config):
    """
    Check that minisite portlet is present or create it
    """
    minisite = request.get('cpskin_minisite', None)
    if not isinstance(minisite, Minisite):
        return

    if minisite.is_in_minisite_mode:
        portal = api.portal.get()
        minisiteRoot = portal.unrestrictedTraverse(minisite.search_path)
        manager = getUtility(IPortletManager,
                             name=u'plone.rightcolumn',
                             context=minisiteRoot)
        assignments = getMultiAdapter((minisiteRoot, manager, ),
                                      IPortletAssignmentMapping)
        if not 'minisite' in assignments:
            assignment = Assignment(name=u"Mini site",
                                    weight=100)
            if not hasattr(assignment, 'collective.weightedportlets'):
                setattr(assignment, 'collective.weightedportlets', PersistentDict())
            getattr(assignment, 'collective.weightedportlets')['weight'] = 100
            assignments['minisite'] = assignment
