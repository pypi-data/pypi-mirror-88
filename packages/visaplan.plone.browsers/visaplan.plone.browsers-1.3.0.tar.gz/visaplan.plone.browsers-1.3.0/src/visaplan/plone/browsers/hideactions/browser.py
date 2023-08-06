# -*- coding: utf-8 -*- äöü
"""\
Browser unitracc@@hideactions: Aktions-Buttons verbergen

TODO: Zweck dokumentieren!
"""
# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.context import get_published_templateid


class IHideActions(Interface):
    """ """

    pass


class Browser(BrowserView):

    implements(IHideActions)

    def __call__(self):
        """ """
        context = self.context
        if context.portal_type in ['UnitraccAuthor',
                                   'UnitraccContact',
                                   ]:
            return True
        if get_published_templateid(context) in ['listing_news',
                                                 ]:
            return True
