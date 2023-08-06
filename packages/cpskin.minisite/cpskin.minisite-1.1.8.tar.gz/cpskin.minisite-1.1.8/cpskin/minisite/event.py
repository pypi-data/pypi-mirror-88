# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.interface import Interface


class IMinisiteMarkedEvent(Interface):
    """
    Marker interface for a marked event on a minisite
    """


class MinisiteMarkedEvent(object):
    implements(IMinisiteMarkedEvent)

    def __init__(self, minisite):
        self.minisite = minisite
