# -*- coding: utf-8 -*-
from cpskin.minisite.interfaces import IMinisiteRoot
from plone import api
from zope.interface import noLongerProvides


def uninstall(context):
    brains = api.content.find(object_provides=IMinisiteRoot.__identifier__)
    for brain in brains:
        obj = brain.getObject()
        noLongerProvides(obj, IMinisiteRoot)
