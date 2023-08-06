# -*- coding: utf-8 -*- äöü
## integriert in --> @@subportal!
# Python compatibility:
from __future__ import absolute_import

# Zope:
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements


class ILogo(Interface):

    def getLogo():
        """
        Gib den Namen der zu verwendenden Logo-Graphik zurück
        """


class Browser(BrowserView):

    implements(ILogo)

    def getLogo(self):
        """
        Gib den Namen der zu verwendenden Logo-Graphik zurück,
        in Abhängigkeit von
        - @@subportal.get_current_info()['logo']
        - Top-Level-Domäne
        """
        context = self.context
        # from visaplan.plone.tools.context import getActiveLanguage
        # langCode = getActiveLanguage(context)
        subportal = context.getBrowser('subportal')

        dict_ = subportal.get_current_info()

        if dict_.get('logo'):
            return dict_['logo']

        portal = getToolByName(context, 'portal_url').getPortalObject()
        domain_ending = portal.absolute_url().split('.')[-1]
        if (domain_ending != 'com'
            and not portal.restrictedTraverse('logo-' + domain_ending + '.jpg', None)
            ):
            domain_ending = 'com'

        return 'logo-' + domain_ending + '.jpg'
