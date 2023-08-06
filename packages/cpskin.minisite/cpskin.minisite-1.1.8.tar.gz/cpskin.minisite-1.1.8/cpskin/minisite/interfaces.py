# -*- coding: utf-8 -*-
from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IInMinisiteBase(IThemeSpecific):
    """Marker interface set on request after traversal in a minisite.
    """


class IInPortal(IInMinisiteBase):
    """Marker interface set on request after traversal in a minisite.

    Request comes with the portal domain.
    """


class IInMinisite(IInMinisiteBase):
    """Marker interface set on request after traversal in a minisite.

    Request comes with the minisite domain.
    """


class IMinisiteConfig(Interface):
    """Minisite data"""


class IMinisiteRoot(Interface):
    """Minisite Root"""
