# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et tw=72 cc=+8
# Python compatibility:
from __future__ import absolute_import

# Zope:
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements

# ------------------------------------------- [ Daten ... [
SCALING = '120x120'
DEFAULT_IMG_NAME = 'article_default_%(SCALING)s.jpg' % globals()
# ------------------------------------------- ] ... Daten ]


class IDefaultImage(Interface):

    def get():
        """ """


class Browser(BrowserView):

    implements(IDefaultImage)

    def get(self):
        """ """
        context = self.context

        # getAdapter: für aufrufenden Kontext
        portal = getToolByName(context, 'portal_url').getPortalObject()

        data = ''
        sm = portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()
        try:
            form = context.REQUEST.form
            uid = form.get('uid')

            #Because we set the security to a master user we only allow one scaling to be delivered
            form.update({'scaling': SCALING})

            rc = getToolByName(portal, 'reference_catalog')
            context = rc.lookupObject(uid)
            # getBrowser: für aus übergebener UID ermittelten Kontext
            portal_type = context.portal_type

            if portal_type == 'UnitraccNews':
                browser = context.getBrowser('news')
                data = browser.getImage(context.UID())
            elif portal_type == 'UnitraccArticle':
                browser = context.getBrowser('article')
                #returns an url
                url = browser.getFirstImage(context.getHereAsBrain(), SCALING)

                #is it an url we can use
                split_url = url.split('/')
                if split_url[2:]:
                    uid = split_url[2]
                    object_ = rc.lookupObject(uid)
                    if object_:
                        browser = object_.getBrowser('scaling')
                        data = browser.get()
                    else:
                        data = str(context.restrictedTraverse(DEFAULT_IMG_NAME)._data)
            elif portal_type in ('UnitraccImage',
                                 'UnitraccAnimation',
                                 ):
                browser = context.getBrowser('scaling')
                data = browser.get()
            elif portal_type == 'Document':
                brain = context.getBrowser('book').getBookFolderAsBrain()
                if brain:
                    brains = context.getBrowser('stage').getAsBrains('illustration', brain.UID)
                    if brains:
                        form.update({'scaling': SCALING})
                        data = brains[0].getObject().getBrowser('scaling').get()
        finally:
            sm.setOld()
            return data
