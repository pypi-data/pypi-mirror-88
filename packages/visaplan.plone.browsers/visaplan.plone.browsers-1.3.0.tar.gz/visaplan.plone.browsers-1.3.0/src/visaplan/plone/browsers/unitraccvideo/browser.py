# -*- coding: utf-8 -*- äöü vim: sts=4 sw=4 si et
# Python compatibility:
from __future__ import absolute_import

# Standard library:
import xml.etree.cElementTree as cET

# Zope:
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName

# 3rd party:
from tomcom.tcconvert.browser import Browser as BrowserView

# visaplan:
from visaplan.plone.base import Interface, implements
from visaplan.plone.tools.context import message


class IUnitraccVideo(Interface):

    def get_streaming_info():
        """ """

    def stream():
        """ """

    def update_ogg():
        """ """


class Browser(BrowserView):

    implements(IUnitraccVideo)

    cache_duration = 3600

    def _set_custom(self):
        """ """
        context = self.context
        root = self._get_root()

        field = context.getField('file')
        type_, subtype = field.getContentType(context).split('/')

        element = cET.Element('target_field')
        element.text = 'ogg'
        root.append(element)

        element = cET.Element('source_field')
        element.text = 'file'
        root.append(element)

        element = cET.Element('new_format')
        element.text = 'ogg'
        root.append(element)

        element = cET.Element('type')
        element.text = type_
        root.append(element)

        element = cET.Element('file_name')
        element.text = field.getFilename(context)
        root.append(element)

    def _get_streaming_dict(self, context, name):
        field = context.getField('file')
        size = field.get_size(context)
        if size:
            return {
                'field_name':   name,
                'content_type': field.getContentType(context),
                }
        return None

    def get_streaming_info(self):

        context = self.context
        list_ = []

        dic = self._get_streaming_dict(context, 'file')
        if dic is not None:
            list_.append(dic)

        dic = self._get_streaming_dict(context, 'ogg')
        if dic is not None:
            list_.append(dic)

        return list_

    def stream(self):
        """ """
        context = self.context
        request = context.REQUEST
        form = request.form
        field_name = form.get('field_name')
        field = context.getField(field_name)
        file = field.get(context)
        return file.index_html(request, request.RESPONSE)

    def update_ogg(self):
        """ """
        context = self.context

        if not getToolByName(context, 'portal_membership').checkPermission('Modify portal content', context):
            raise Unauthorized

        context.setOgg(None)

        self.send()

        message(context,
                'Changes saved.')

        return context.REQUEST.RESPONSE.redirect(context.absolute_url() + '/view')
