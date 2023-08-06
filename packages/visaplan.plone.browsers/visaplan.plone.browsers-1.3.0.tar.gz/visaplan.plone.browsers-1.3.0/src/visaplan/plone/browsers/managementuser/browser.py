# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements


class IManagementUser(Interface):

    pass


class Browser(BrowserView):

    implements(IManagementUser)
