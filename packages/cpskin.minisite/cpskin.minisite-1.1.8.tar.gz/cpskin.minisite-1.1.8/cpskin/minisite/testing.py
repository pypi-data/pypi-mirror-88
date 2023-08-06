# -*- coding: utf-8 -*-
# from plone import api
from cpskin.core.behaviors.metadata import IHiddenTags
from cpskin.core.utils import add_behavior
from plone.app.controlpanel.security import ISecuritySchema
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from plone.testing import z2
import cpskin.minisite


class CPSkinMinisiteLayer(PloneWithPackageLayer):

    def setUpZope(self, app, configurationContext):
        super(CPSkinMinisiteLayer, self).setUpZope(
            app,
            configurationContext)
        z2.installProduct(app, 'Products.DateRecurringIndex')

    def tearDownZope(self, app):
        # Uninstall products installed above
        z2.uninstallProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
        # super(CPSkinMinisiteLayer).setUpPloneSite(portal)
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')
        # applyProfile(portal, 'plone.app.contenttypes:plone-content')
        applyProfile(portal, 'cpskin.minisite:testing')
        add_behavior('Document', IHiddenTags.__identifier__)
        ISecuritySchema(portal).set_enable_self_reg(True)


CPSKIN_MINISITE = CPSkinMinisiteLayer(
    name='CPSKIN_MINISITE',
    zcml_package=cpskin.minisite,
    zcml_filename='testing.zcml',
    gs_profile_id='cpskin.minisite:testing',
)

CPSKIN_MINISITE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_MINISITE,),
    name='CPSKIN_MINISITE_INTEGRATION_TESTING'
)
CPSKIN_MINISITE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CPSKIN_MINISITE, z2.ZSERVER_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE),
    name='CPSKIN_MINISITE_FUNCTIONAL_TESTING'
)
