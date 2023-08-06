# -*- coding: utf-8 -*-
from cpskin.minisite.testing import CPSKIN_MINISITE_FUNCTIONAL_TESTING
from plone.testing import layered

import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('robot_test.txt'),
                layer=CPSKIN_MINISITE_FUNCTIONAL_TESTING)
    ])
    return suite
