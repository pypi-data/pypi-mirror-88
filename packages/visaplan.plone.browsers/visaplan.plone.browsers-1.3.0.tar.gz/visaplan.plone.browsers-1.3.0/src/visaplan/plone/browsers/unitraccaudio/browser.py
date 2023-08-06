# -*- coding: utf-8 -*- äöü vim: sts=4 sw=4 si et
# Python compatibility:
from __future__ import absolute_import

# Standard library:
import xml.etree.cElementTree as cET

# 3rd party:
from tomcom.tcconvert.browser import Browser as BrowserView

# visaplan:
from visaplan.plone.base import Interface, implements


class IUnitraccAudio(Interface):

    def get_streaming_info():
        """ """

    def stream():
        """ """

    def get_script_content(absurl, uid):
        """
        Gib Javascript-Code zurück
        """


class Browser(BrowserView):

    implements(IUnitraccAudio)

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

    def get_script_content(self, absurl, uid):
        """
        Gib Javascript-Code zurück
        """
        return """\
    if (document.createElement('audio').canPlayType) {
        if (!document.createElement('audio').canPlayType('audio/mpeg') &&
            !document.createElement('audio').canPlayType('audio/ogg')) {
                swfobject.embedSWF("player_mp3_mini.swf",
                     "player_fallback-%(uid)s", "200", "20", "9.0.0", "",
                     {"mp3":"%(absurl)s/@@unitraccaudio/stream?field_name=file"},
                     {"bgcolor":"#5C595A"}
                );
                swfobject.embedSWF("/player_mp3_mini.swf",
                     "custom_player_fallback-%(uid)s", "200", "20", "9.0.0", "",
                     {"mp3":"%(absurl)s/@@unitraccaudio/stream?field_name=file"},
                     {"bgcolor":"#5C595A"}
                );
        document.getElementById('audio_with_controls-%(uid)s').style.display = 'none';
        } else {
                // HTML5 audio + mp3 support
                //document.getElementById('player').style.display = 'block';
        }
    }
    """ % locals()
