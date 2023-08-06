# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements


class ICookie(Interface):

    def set(key, value):
        """set cookie"""

    def get(key):
        """get cookie"""


class Browser(BrowserView):

    implements(ICookie)

    def get(self, key):
        """ """
        return self.context.REQUEST.cookies.get(key, '')

    def set(self, key, value):
        """ """
        REQUEST = self.context.REQUEST
        cookies = REQUEST.cookies.get(key, '')
        if key in REQUEST.cookies:
            del REQUEST.cookies[key]
        REQUEST.RESPONSE.setCookie(key, value, path='/')

    def delete(self, key):
        if key in self.context.REQUEST.cookies:
            del self.context.REQUEST.cookies[key]
