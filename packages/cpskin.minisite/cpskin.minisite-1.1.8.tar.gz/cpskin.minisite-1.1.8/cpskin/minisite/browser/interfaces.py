from zope import schema
from zope.interface import Interface


class IHNavigationActivationView(Interface):
    """ Horizontal navigation activation """

    can_enable_hnavigation = schema.Bool(
        u'Can enable horizontal navigation viewlet',
        readonly=True
    )

    can_disable_hnavigation = schema.Bool(
        u'Can disable horizontal navigation viewlet',
        readonly=True
    )

    def enable_hnavigation():
        """ Enable horizontal navigation viewlet
        """

    def disable_hnavigation():
        """ Disable horizontal navigation viewlet
        """


class IHNavigationActivated(Interface):
    """
    marker interface to tell if Horizontal Navigation is activate
    """
