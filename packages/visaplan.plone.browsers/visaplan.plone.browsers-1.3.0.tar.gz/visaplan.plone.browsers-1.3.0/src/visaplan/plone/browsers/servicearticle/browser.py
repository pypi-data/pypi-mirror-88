# Python compatibility:
from __future__ import absolute_import

# Zope:
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements


class IServiceArticle(Interface):

    pass


class Browser(BrowserView):

    implements(IServiceArticle)

    def __call__(self):
        """ """
        context = self.context

        portal = getToolByName(context, 'portal_url').getPortalObject()
        sm = portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()

        pc = getToolByName(context, 'portal_catalog')._catalog
        browser = context.getBrowser('news')
        queryDate = DateTime() - browser.days

        query = {}
        query['portal_type'] = 'UnitraccArticle'
        query['created'] = {'query': queryDate,
                          'range': 'max'}
        query['effective'] = {'query': queryDate,
                            'range': 'max'}
        query['review_state'] = ['published', 'inherit']

        for brain in pc(query):
            object_ = brain.getObject()
            object_.getBrowser('workflow').change('make_visible')

        sm.setOld()

        return True
