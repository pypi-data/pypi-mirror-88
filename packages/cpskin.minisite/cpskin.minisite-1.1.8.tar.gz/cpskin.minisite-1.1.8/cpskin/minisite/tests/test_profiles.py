import unittest

from plone.app.testing import applyProfile

from cpskin.minisite.testing import CPSKIN_MINISITE_INTEGRATION_TESTING


class TestProfiles(unittest.TestCase):

    layer = CPSKIN_MINISITE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_uninstall(self):
        applyProfile(self.portal, 'cpskin.minisite:uninstall')

    def test_reinstall(self):
        applyProfile(self.portal, 'cpskin.minisite:uninstall')
        applyProfile(self.portal, 'cpskin.minisite:default')
