# -*- coding: utf-8 -*-
"""
@@languageredirector:
Weiterleitung zum zur Sprache passenden (virtuellen) Host

TODO:
- hartcodierte Zuordnungen konfigurierbar machen
  - am besten je Subportal
- direkt Plone-Tools verwenden
"""
# Python compatibility:
from __future__ import absolute_import

# Zope:
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.context import getActiveLanguage


class ILanguageRedirector(Interface):

    """
    Browser wird durch Kontext aufgerufen
    """


class Browser(BrowserView):

    implements(ILanguageRedirector)

    def __call__(self):
        """ """
        context = self.context
        langCode = getActiveLanguage(context)
        redirect = context.REQUEST.RESPONSE.redirect

        portal_url = getToolByName(context, 'plone_portal_state').portal_url()
        protocol = portal_url.split(':')[0] + '://'

        if langCode == 'de':
            if portal_url.find('unitracc.de') == -1:
                return redirect(protocol + 'unitracc.de')
            return

        if langCode == 'en':
            if portal_url.find('unitracc.com') == -1:
                return redirect(protocol + 'unitracc.com')
            return

        if langCode == 'es':
            if portal_url.find('unitracc.es') == -1:
                return redirect(protocol + 'unitracc.es')
            return
