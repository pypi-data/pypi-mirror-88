# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements


class ICountryCodeToCountry(Interface):

    pass


class Browser(BrowserView):

    implements(ICountryCodeToCountry)

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)

        self.dict_ = {}

        for k, v in context.getBrowser('voccountry').get():
            self.dict_[k] = v

    def __call__(self, string_):
        return self.dict_.get(string_, string_)
