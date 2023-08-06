# Python compatibility:
from __future__ import absolute_import

# Zope:
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements


class IServiceNews(Interface):

    pass


class Browser(BrowserView):

    implements(IServiceNews)

    def __call__(self):
        """ """
        context=self.context

        portal = getToolByName(context, 'portal_url').getPortalObject()
        sm=portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()

        try:
            pc = getToolByName(portal, 'portal_catalog')._catalog
            browser=context.getBrowser('news')
            queryDate=DateTime()-browser.days

            query={}
            query['portal_type']='UnitraccNews'
            query['created']={'query':queryDate,
                              'range':'max'}
            query['effective']={'query':queryDate,
                                'range':'max'}
            query['review_state']=['published','inherit']

            for brain in pc(query):
                object_=brain.getObject()
                object_.getBrowser('workflow').change('make_visible')

        finally:
            sm.setOld()

        return True
