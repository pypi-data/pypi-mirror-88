import unittest
from zope.component import queryMultiAdapter
from zope.viewlet.interfaces import IViewletManager
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from Products.Five.browser import BrowserView as View
from cpskin.minisite.minisite import MinisiteConfig, decorateRequest
from cpskin.minisite.testing import CPSKIN_MINISITE_INTEGRATION_TESTING
from plone import api


class TestMyViewlet(unittest.TestCase):
    """ test demonstrates that registration variables worked
    """

    layer = CPSKIN_MINISITE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.app = self.layer['app']
        self.minisite_folder = api.content.create(
            type='Folder',
            id='test_minisite',
            title='test_minisite',
            container=self.portal)
        minisite = MinisiteConfig(
            main_portal_url='http://localhost',
            minisite_url='http://nohost',
            search_path='/plone/test_minisite',
            filename='minisite_config.txt',
        )
        self.request = self.app.REQUEST
        decorateRequest(self.request, minisite)

    def test_viewlet_is_present(self):
        """ looking up and updating the manager should list our viewlet
        """
        # we need a context and request
        minisite_subfolder = api.content.create(
            type='Folder',
            id='minisite_subfolder',
            title='minisite_subfolder',
            container=self.minisite_folder)
        request = self.request
        context = self.minisite_folder

        # viewlet managers also require a view object for adaptation
        view = View(context, request)

        # finally, you need the name of the manager you want to find
        manager_name = 'plone.portaltop'

        # viewlet managers are found by Multi-Adapter lookup
        manager = queryMultiAdapter((context, request, view),
                                    IViewletManager,
                                    manager_name,
                                    default=None)
        self.assertIsNotNone(manager)

        # calling update() on a manager causes it to set up its viewlets
        manager.update()

        # now our viewlet should be in the list of viewlets for the manager
        # we can verify this by looking for a viewlet with the name we used
        # to register the viewlet in zcml
        my_viewlet = [v for v in manager.viewlets if v.__name__ == 'cpskin.minisitemenu']
        self.assertEqual(len(my_viewlet), 1)

    def test_viewlet_menu_contents(self):
        """ looking up and updating the manager should list our viewlet
        """
        non_minisite_subfolder = api.content.create(
            type='Folder',
            id='non_minisite_subfolder',
            title='non_minisite_subfolder',
            container=self.portal)

        minisite_subfolder = api.content.create(
            type='Folder',
            id='minisite_subfolder',
            title='minisite_subfolder',
            container=self.minisite_folder)

        request = self.request
        context = self.minisite_folder

        view = View(context, request)
        manager_name = 'plone.portaltop'
        manager = queryMultiAdapter((context, request, view),
                                    IViewletManager,
                                    manager_name,
                                    default=None)
        self.assertIsNotNone(manager)
        manager.update()
        viewlets = [v for v in manager.viewlets if v.__name__ == 'cpskin.minisitemenu']
        ms_viewlet = viewlets[0]
        ids = [item['id'] for item in ms_viewlet.portal_tabs]
        self.assertIn(minisite_subfolder.id, ids)
        self.assertNotIn(non_minisite_subfolder.id, ids)
