# -*- coding: utf-8 -*- Umlaute: ÄÖÜäöüß
# Python compatibility:
from __future__ import absolute_import

# Zope:
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.search import language_spec

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport

logger, debug_active, DEBUG = getLogSupport(fn=__file__)


class IGlossaryBrowser(Interface):

    def search():
        """ """


class Browser(BrowserView):

    implements(IGlossaryBrowser)

    def search(self):
        """ """
        context = self.context
        portal = getToolByName(context, 'portal_url').getPortalObject()

        sm = portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()

        try:
            form = context.REQUEST.form
            pc = getToolByName(context, 'portal_catalog')
            txng = context.getBrowser('txng')
            query = {}

            queryString = form.get('SearchableText', '')
            DEBUG('search: queryString (1) = %(queryString)r', locals())
            if queryString and type(queryString) == type(''):
                queryString = txng.get(queryString)
                DEBUG('search: queryString (2.txng.get) = %(queryString)r', locals())
                if queryString:
                    query['SearchableText'] = queryString

            query['portal_type'] = 'UnitraccGlossary'
            query['getExcludeFromNav'] = False
            query['sort_on'] = 'sortable_title'
            query['effective'] = {'query': DateTime(),
                                  'range': 'max'}

            query['review_state'] = ['inherit', 'published', 'visible']

            langs = language_spec(form=form,
                                  # aktuelles Verhalten (schlau so?):
                                  default_to_all=False,
                                  context=context)
            if langs:
                query['Language'] = langs
            DEBUG('search: query (3) = %(query)s', locals())
            brains = pc(query)
            DEBUG('search: query (4) = %d Treffer', len(brains))

            return brains
        finally:
            sm.setOld()
