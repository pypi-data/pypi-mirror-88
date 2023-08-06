# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements


class IIsThreeColumnLayoutVisible(Interface):
    """ """
    pass


class Browser(BrowserView):

    implements(IIsThreeColumnLayoutVisible)

    def __call__(self):
        """ """
        context = self.context
        list_ = context.getPhysicalPath()
        if len(list_) > 2:
            desktop_id = context.getBrowser('unitraccfeature').desktop_id()
            if list_[2] == desktop_id:
                return True
