# Python compatibility:
from __future__ import absolute_import

# Zope:
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements


class IRedirector(Interface):

    pass


class Browser(BrowserView):

    implements(IRedirector)

    def __call__(self):
        """ """
        context = self.context
        portal = getToolByName(context, 'portal_url').getPortalObject()
        request = context.REQUEST
        if portal.absolute_url().find('www.') != -1:
            url = request['URL']
            url = url.replace('www.', '')

            if request['QUERY_STRING']:
                url += '?'
                url += request['QUERY_STRING']
            return context.REQUEST.RESPONSE.redirect(url)
