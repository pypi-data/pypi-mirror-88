# Python compatibility:
from __future__ import absolute_import

# Standard library:
import json

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements


class IJson(Interface):

    def encode(value):
        """ """

    def decode(value):
        """ """


class Browser(BrowserView):

    implements(IJson)

    def encode(self, value):
        return json.dumps(value)

    def decode(self, value):
        return json.loads(value)
