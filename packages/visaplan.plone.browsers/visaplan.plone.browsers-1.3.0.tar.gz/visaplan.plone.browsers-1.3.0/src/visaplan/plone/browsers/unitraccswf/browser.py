# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements


class IUnitraccSwf(Interface):

    def get_size(self):
        """ """


class Browser(BrowserView):

    implements(IUnitraccSwf)

    def get_size(self, max_width=640, max_height=480):
        """ """
        context = self.context

        width_ = context.getWidth()
        height_ = context.getWidth()
        dict_ = {}
        if not width_ and not height_:
            result = context.getAdapter('swfinfo')()
            if float(result.get('width', 0.0)) > max_width:
                dict_['height'] = int(float(max_width) / (float(result['width']) / float(result['height'])))
                dict_['width'] = max_width

            return dict_
        else:
            dict_['width'] = width_
            dict_['height'] = height_
            return dict_
