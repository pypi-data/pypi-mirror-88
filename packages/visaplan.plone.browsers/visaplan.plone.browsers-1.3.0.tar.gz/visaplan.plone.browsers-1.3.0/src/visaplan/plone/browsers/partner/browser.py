# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements


class IPartner(Interface):

    def get(brain):
        """ """


class Browser(BrowserView):

    implements(IPartner)

    def get(self, brain):
        """ """
        context = self.context
        stage = context.getBrowser('stage')

        if brain.getPartOf:
            return stage.getAsBrains('unitracc-partner', brain.getPartOf)
        else:
            return stage.getAsBrains('unitracc-partner', brain.UID)
