# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.context import getSupportedLanguageTuples


class IUserLanguage(Interface):

    def get():
        """ """


class Browser(BrowserView):

    implements(IUserLanguage)

    def get(self):
        """ """
        context = self.context
        return getSupportedLanguageTuples(context)
