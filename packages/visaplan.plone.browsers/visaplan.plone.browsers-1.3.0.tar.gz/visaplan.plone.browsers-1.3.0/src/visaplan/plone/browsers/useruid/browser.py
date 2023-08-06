# Python compatibility:
from __future__ import absolute_import

# Standard library:
from hashlib import md5

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements


class IUserUid(Interface):

    def set():
        """
        Erzeuge das Cookie 'useruid', falls noch nicht vorhanden
        """

    def get():
        """
        Lies das Cookie 'useruid' aus
        """


class Browser(BrowserView):

    implements(IUserUid)

    key = 'useruid'  # hier nicht mehr verwendet

    def set(self):
        """
        Erzeuge das Cookie 'useruid', falls noch nicht vorhanden
        """
        REQUEST = self.context.REQUEST
        cookies = REQUEST.cookies
        if 'useruid' not in cookies:
            get = REQUEST.get
            value = md5(get('HTTP_X_FORWARDED_FOR', '') +
                        get('HTTP_USER_AGENT', '') +
                        get('channel.creation_time', '')
                        ).hexdigest()
            REQUEST.RESPONSE.setCookie('useruid', value, path='/')

    def get(self):
        """
        Lies das Cookie 'useruid' aus
        """
        return self.context.REQUEST.cookies.get('useruid', '')
