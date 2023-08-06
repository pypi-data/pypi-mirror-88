# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

# Standard library:
import unittest

# Zope:
from zope.component import getMultiAdapter
from zope.component.interfaces import ComponentLookupError

# Plone:
from plone import api
from plone.app.testing import TEST_USER_ID, setRoles

# visaplan:
from visaplan.plone.browsers.testing import (
    VISAPLAN_PLONE_BROWSERS_FUNCTIONAL_TESTING,
    VISAPLAN_PLONE_BROWSERS_INTEGRATION_TESTING,
    )


class ViewsIntegrationTest(unittest.TestCase):

    layer = VISAPLAN_PLONE_BROWSERS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Folder', 'other-folder')
        api.content.create(self.portal, 'Collection', 'my-collection')

    def test_book_agenda_embed_is_registered(self):
        view = getMultiAdapter(
            (self.portal['other-folder'], self.portal.REQUEST),
            name='book-agenda-embed'
        )
        self.assertTrue(view(), 'book-agenda-embed is not found')
        self.assertTrue(
            'Sample View' in view(),
            'Sample View is not found in book-agenda-embed'
        )
        self.assertTrue(
            'Sample View' in view(),
            'A small message is not found in book-agenda-embed'
        )

    def test_book_agenda_embed_in_my_collection(self):
        with self.assertRaises(ComponentLookupError):
            getMultiAdapter(
                (self.portal['my-collection'], self.portal.REQUEST),
                name='book-agenda-embed'
            )


class ViewsFunctionalTest(unittest.TestCase):

    layer = VISAPLAN_PLONE_BROWSERS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
