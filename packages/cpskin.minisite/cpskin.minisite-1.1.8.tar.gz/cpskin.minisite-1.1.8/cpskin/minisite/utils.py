# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from cpskin.minisite.interfaces import IMinisiteConfig
from plone import api
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_hasattr
from zExceptions import NotFound
from zExceptions import Unauthorized
from zope.component import getUtilitiesFor


def get_minisite_object(request):
    minisite = request.get('cpskin_minisite', None)
    if not minisite:
        return None
    return api.content.get(minisite.search_path)


def get_minisite_path(request):
    minisite = request.get('cpskin_minisite', None)
    if not minisite:
        return None
    return minisite.search_path


def get_minisite_navigation_level(minisite_obj):
    portal = api.portal.get()
    portal_physical_path = portal.getPhysicalPath()
    minisite_physical_path = minisite_obj.getPhysicalPath()
    minisite_path = [elem for elem in list(minisite_physical_path) if elem not in list(portal_physical_path)]  # noqa
    return len(minisite_path)


def list_minisites(portal):
    portal_path = '/'.join(portal.getPhysicalPath())
    configs = getUtilitiesFor(IMinisiteConfig, portal)
    result = [
        config for name, config in configs
        if config.search_path.startswith(portal_path)
    ]
    return result


def url_in_portal_mode(context, request):
    portal_url = getToolByName(context, 'portal_url')
    relative_url = portal_url.getRelativeContentURL(context)
    portal = portal_url.getPortalObject()
    main_portal_url = request.cpskin_minisite.main_portal_url
    minisite_url = request.cpskin_minisite.minisite_url
    root_url = portal.absolute_url()
    root_url_in_portal_mode = root_url.replace(
        minisite_url,
        main_portal_url
    )
    return '/'.join((root_url_in_portal_mode, relative_url))


def get_acquired_base_object(minisite_obj, path):
    obj = minisite_obj
    path = path.split('@@')[0]
    contents = path.strip('/').split('/')
    parent_id = contents[0]
    child_id = len(contents) > 1 and contents[1] or None
    while not IPloneSiteRoot.providedBy(obj):
        parent = aq_parent(aq_inner(obj))
        if parent is None:
            break
        obj = parent
        if safe_hasattr(aq_base(obj), parent_id):
            if not child_id:
                return obj
            container = getattr(aq_base(obj), parent_id)
            if safe_hasattr(container, child_id):
                try:
                    obj_url = '/'.join(obj.getPhysicalPath())
                    full_url = "{0}{1}".format(
                        obj_url,
                        path,
                    )
                    api.content.get(full_url)
                except Unauthorized:
                    continue
                except NotFound:
                    continue
                else:
                    return obj
