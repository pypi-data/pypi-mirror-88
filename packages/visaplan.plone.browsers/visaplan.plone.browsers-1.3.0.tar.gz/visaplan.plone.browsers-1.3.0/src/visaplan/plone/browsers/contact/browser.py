# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=79
# Python compatibility:
from __future__ import absolute_import

# Zope:
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.brains import make_collector
from visaplan.plone.tools.context import getbrain

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport

logger, debug_active, DEBUG = getLogSupport(fn=__file__)


_contactCompany = make_collector(use=['getContactCompany'])
_contactPerson = make_collector(use=['getContactAcademicTitle',
                                     'getContactFirstname',
                                     'getContactLastname',
                                     ],
                                any=['getContactFirstname',
                                     'getContactLastname',
                                     ])


class IContactBrowser(Interface):

    def getRelated():
        """Return related contact of context if exists"""

    def getRelatedByUid(self, uid):  # !! deklariert, aber nicht implementiert!
        """ """

    def search():
        """ """

    def getImage():
        """ """

    def getPartner():
        """ """

    def getContactByUid(uid):
        """ """

    def getContactTitleByUid(uid):
        """ """

    def isContactVisible():
        """ """

    def getContactTitle(brain):
        """
        Gib die Kontaktperson als Zeichenkette zurück, sofern Vor- oder
        Nachname angegeben; ansonsten die Firma
        """

    def getContactPerson(brain):
        """
        Gib die Kontaktperson als Zeichenkette zurück, oder None
        """

    def getContactCompany(brain):
        """
        Gib den Firmenkontakt als Zeichenkette zurück, oder None
        """


class Browser(BrowserView):

    implements(IContactBrowser)

    UID = 'a8bbe3be69129c027e1a1c584bc925cd'    # /management/kontakte

    def getRelated(self):
        context = self.context
        if hasattr(context, 'UID'):
            return self.getRelatedByUid(context.UID())

    def getContactByUid(self, uid):
        """ """
        context = self.context
        return getbrain(context, uid)

    def getContactTitleByUid(self, uid):
        context = self.context
        ps = context.getBrowser('ps')
        return ps._get(uid, {}).get('title')

    def search(self):
        """ """
        context = self.context
        form = context.REQUEST.form
        pc = getToolByName(context, 'portal_catalog')
        txng = context.getBrowser('txng')

        queryString = form.get('SearchableText', '')
        DEBUG('search: queryString (1) = %(queryString)r', locals())
        queryString = txng.processWords(queryString)
        DEBUG('search: queryString (2.txng) = %(queryString)r', locals())

        query = {}
        query['portal_type'] = 'UnitraccContact'
        query['SearchableText'] = queryString

        return pc(query)

    def getImage(self):
        """ """
        context = self.context
        scaling = context.getBrowser('scaling')
        data = scaling.get()
        if data:
            return data
        return context.restrictedTraverse('dummy_author.png')._data

    def getPartner(self):
        """ """
        context = self.context
        pc = getToolByName(context, 'portal_catalog')

        query = {}
        query['portal_type'] = 'UnitraccContact'
        query['getCustomSearch'] = 'Partner'

        return [(brain.UID, brain.Title) for brain in pc(query)]

    def isContactVisible(self):
        """ """
        context = self.context
        if context.portal_type in ['UnitraccArticle', 'UnitraccNews', 'UnitraccEvent']:
            for field in context.schema.getSchemataFields('contact'):
                if field.get(context):
                    return True

    def getContactTitle(self, brain):
        """
        Gib die Kontaktperson als Zeichenkette zurück, sofern Vor- oder
        Nachname angegeben; ansonsten die Firma
        """
        return _contactPerson(brain) or _contactCompany(brain)
        # alter Code:
        context = self.context
        if not brain.getContactFirstname and not brain.getContactLastname:
            return brain.getContactCompany
        string_ = ''
        string_ += brain.getContactAcademicTitle
        if string_:
            string_ += ' '
        string_ += brain.getContactFirstname
        if string_:
            string_ += ' '
        string_ += brain.getContactLastname
        return string_

    def getContactPerson(self, brain):
        """
        Gib die Kontaktperson als Zeichenkette zurück, oder None
        """
        return _contactPerson(brain)

    def getContactCompany(self, brain):
        """
        Gib den Firmenkontakt als Zeichenkette zurück, oder None
        """
        return _contactCompany(brain)
