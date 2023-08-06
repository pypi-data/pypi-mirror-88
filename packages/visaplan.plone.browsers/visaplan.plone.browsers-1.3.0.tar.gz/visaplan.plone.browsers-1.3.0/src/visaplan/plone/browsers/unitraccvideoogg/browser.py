# Python compatibility:
from __future__ import absolute_import

# Standard library:
import xml.etree.cElementTree as cET

# Zope:
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName

# 3rd party:
from tomcom.tcconvert.browser import Browser as BrowserView
from tomcom.tcconvert.browser import *

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.context import message as _


class IUnitraccVideoOGG(Interface):

    def update_field():
        """ """


class Browser(BrowserView):

    implements(IUnitraccVideoOGG)

    def update_field(self):
        """ """
        context=self.context

        if not getToolByName(context, 'portal_membership').checkPermission('Modify portal content', context):
            raise Unauthorized

        if context.getSource() or context.getFile():
            context.setOgg(None)

            self.send()

            message(context, 'Changes saved.')

        else:
            message(context, 'Source or mp4 format does not exist.', 'error')

        return context.REQUEST.RESPONSE.redirect(context.REQUEST['HTTP_REFERER'])

    def _set_custom(self):
        """ """
        context=self.context
        root=self._get_root()

        element=cET.Element('target_field')
        element.text='ogg'
        root.append(element)

        element=cET.Element('source_field')
        element.text='source'
        root.append(element)

        element=cET.Element('new_format')
        element.text='ogg'
        root.append(element)

        element=cET.Element('type')
        element.text='video'
        root.append(element)

        element=cET.Element('file_name')
        element.text=context.getField('source').getFilename(context)
        root.append(element)
