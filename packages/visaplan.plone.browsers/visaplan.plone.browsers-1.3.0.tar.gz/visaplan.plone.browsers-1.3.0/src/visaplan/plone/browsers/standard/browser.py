# Python compatibility:
from __future__ import absolute_import

# Zope:
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport

logger, debug_active, DEBUG = getLogSupport(fn=__file__)


class IStandardBrowser(Interface):

    def search():
        """ """


class Browser(BrowserView):

    implements(IStandardBrowser)

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

            queryString = form.get('SearchableText', '')
            DEBUG('search: queryString (1) = %(queryString)r', locals())
            queryString = txng.processWords(queryString).strip()
            DEBUG('search: queryString (2.txng) = %(queryString)r', locals())
            if queryString:
                queryString = '*' + queryString + '*'

            query = {
                'portal_type': 'UnitraccStandard',
                'getExcludeFromNav': False,
                'sort_on': 'sortable_title',
                'review_state': ['visible', 'inherit',
                                 'published'],  # TH: warum nicht auch 'restricted'?
                'effective': {'query': DateTime(),
                              'range': 'max'},
                }

            if form.get('source', ''):
                query['getCustomSearch'] = ['source=' + form.get('source', '')]

            if queryString:
                query['SearchableText'] = queryString

            if form.get('language', ''):
                if form['language'] == 'all':
                    # TH 16.3.2017: Warum nicht einfach weglassen?
                    pl = getToolByName(context, 'portal_languages')
                    langs = [x[0] for x in pl.listSupportedLanguages()]
                else:
                    langs = [form['language']]
                query['Language'] = langs

            if form.get('Subject', ''):
                query['Subject'] = form.get('Subject', '')
            brains = pc(query)
        finally:
            sm.setOld()

        return brains
