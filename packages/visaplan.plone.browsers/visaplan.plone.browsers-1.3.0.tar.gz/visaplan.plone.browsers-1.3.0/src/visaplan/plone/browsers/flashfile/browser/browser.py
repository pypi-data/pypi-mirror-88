# -*- coding: utf-8 -*-

# Python compatibility:
from __future__ import absolute_import

from six.moves import range

# Standard library:
import os
import re
import struct
import zlib
from os.path import exists, getsize, join

# Zope:
from App.config import getConfiguration
from OFS.Image import File
from Products.Archetypes.event import ObjectEditedEvent
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope import event
from zope.interface import Interface, implements

# visaplan:
from visaplan.plone.tools.context import message

# Logging / Debugging:
import logging

logger = logging.getLogger('unitracc@@flashfile')


class IFlashFile(Interface):

    def streamFlvFile():
        """Return file data for streaming a video file"""

    def getContentTypeName():
        """return content type name for content type"""

    def download():
        """Download flv"""

    def getSWFSize(maxSize=0):
        """Parses the header information from an SWF file."""


class Browser(BrowserView):
    implements(IFlashFile)

    def _storage_path(self):
        """ """
        return getConfiguration().product_config.get('flv', {})['flv_dir'] + os.sep

    def _flash_file_path(self, uid=None):
        if uid is None:
            context = self.context
            uid = context.UID()
        return join(self._storage_path(),
                    uid + '_flash_file')

    def streamFlvFile(self):
        """Return file data for streaming a video file"""
        context = self.context
        ffn = self._flash_file_path(context.UID())
        if exists(ffn):
            file_ = File(id=context.getId(),
                         title=context.Title(),
                         file=open(ffn, 'rb'),
                         content_type='video/x-flv')
            return file_.index_html(context.REQUEST, context.REQUEST.RESPONSE)
        else:
            if getConfiguration().product_config.get('flv', {})['active'] == 'True':
                if context.getContentType().startswith('video/'):
                    self._convert()
        return ''

    def getSize(self):
        """ """
        context = self.context
        ffn = self._flash_file_path(context.UID())
        if exists(ffn):
            return context.getObjSize(size=getsize(ffn))
        else:
            return '0'

    def download(self):
        """Download flv"""

        field = self.context.getField('file')
        filename = field.getFilename(self.context).split('.')[0]
        data = self.streamFlvFile()
        REQUEST = self.context.REQUEST
        RESPONSE = REQUEST.RESPONSE
        RESPONSE.setHeader('Content-Disposition',
                           'attachment; filename="%s"' % (filename + '.flv'))
        RESPONSE.setHeader('Content-Type', 'video/x-flv')
        RESPONSE.setHeader('Content-Length', len(data))
        RESPONSE.write(data)

    def getContentTypeName(self):
        """return content type name for content type"""
        content_type = self.context.getContentType()

        mreg = getToolByName(self.context, 'mimetype_registry')
        types = mreg.lookup(content_type)
        return types and types[0].name() or content_type

    def getSWFSize(self, maxSize=0):
        """Parses the header information from an SWF file."""
        context = self.context

        input = self._storage_path() + context.UID() + '_file'

        if hasattr(input, 'read'):
            input.seek(0)
        else:
            input = open(input, 'rb')

        def read_ui8(c):
            return struct.unpack('<B', c)[0]

        def read_ui16(c):
            return struct.unpack('<H', c)[0]

        def read_ui32(c):
            return struct.unpack('<I', c)[0]

        header = {}

        # Read the 3-byte signature field
        signature = ''.join(struct.unpack('<3c', input.read(3)))
        if signature not in ('FWS', 'CWS'):
            raise ValueError('Invalid SWF signature: %s' % signature)

        # Compression
        header['compressed'] = signature.startswith('C')

        # Version
        header['version'] = read_ui8(input.read(1))

        # File size (stored as a 32-bit integer)
        header['size'] = read_ui32(input.read(4))

        # Payload
        buffer = input.read(header['size'])
        if header['compressed']:
            # Unpack the zlib compression
            buffer = zlib.decompress(buffer)

        # Containing rectangle (struct RECT)

        # The number of bits used to store the each of the RECT values are
        # stored in first five bits of the first byte.
        nbits = read_ui8(buffer[0]) >> 3

        current_byte, buffer = read_ui8(buffer[0]), buffer[1:]
        bit_cursor = 5

        for item in 'xmin', 'xmax', 'ymin', 'ymax':
            value = 0
            for value_bit in range(nbits - 1, -1, -1):  # == reversed(range(nbits))
                if (current_byte << bit_cursor) & 0x80:
                    value |= 1 << value_bit
                # Advance the bit cursor to the next bit
                bit_cursor += 1

                if bit_cursor > 7:
                    # We've exhausted the current byte, consume the next one
                    # from the buffer.
                    current_byte, buffer = read_ui8(buffer[0]), buffer[1:]
                    bit_cursor = 0

            # Convert value from TWIPS to a pixel value
            header[item] = value / 20

        header['width'] = header['xmax'] - header['xmin']
        header['height'] = header['ymax'] - header['ymin']

        header['frames'] = read_ui16(buffer[0:2])
        header['fps'] = read_ui16(buffer[2:4])

        input.close()

        dict_ = {}
        dict_['width'] = header['width']
        dict_['height'] = header['height']

        if maxSize:
            if dict_['width'] > dict_['height']:
                factor = int(float(maxSize) / (float(dict_['width']) / 100))
                dict_['width'] = maxSize
                dict_['height'] = int(float(dict_['height']) * (float(factor) / 100))
            else:
                factor = int(float(maxSize) / (float(dict_['height']) / 100))
                dict_['height'] = maxSize
                dict_['width'] = int(float(dict_['width']) * (float(factor) / 100))

        return dict_

    def _convert(self):
        """ """
        context = self.context

        blob_ = context.getField('file').get(context).blob
        blob_._p_deactivate()
        try:
            fshelper = blob_._p_jar._storage.fshelper
        except AttributeError as e:
            logger.error('error converting %(context)r:', locals())
            logger.exception(e)
            return
        # TH: warum hier den Browser holen?! flashfile ist der hiesige!
        # base_path = context.getBrowser('flashfile')._storage_path() + context.UID() + '_flash_file'
        base_path = self._flash_file_path(context.UID())
        dict_ = {}
        dict_['input'] = fshelper.getBlobFilename(blob_._p_oid, blob_._p_serial)
        dict_['output'] = output_path = base_path + '.flv'

        # TODO: - Kommando als Liste (ohne Quoting-Probleme) ausführen
        #       - Was macht dieses Kommando genau?
        #       - ffmpeg: Pfad konfigurieren, oder aus thebops...ToolsHub?
        string_ = 'ffmpeg -i %(input)s -ar 22050 -ab 96k -qscale 6 %(output)s'
        command = string_ % dict_
        logger.info('execute: %(command)s', locals())
        try:
            fp = os.popen(command)
            fp.read()
            fp.close()
            logger.info('OK; mv %s %s', dict_['output'], base_path)
            os.rename(dict_['output'], base_path)
            logger.info('mv OK')
        except OSError as e:
            logger.error('Error executing %(command)r:', locals())
            logger.exception(e)
            message(context, 'Error converting video',
                             'error')
        else:
            logger.info('converted %(context)r (%(output_path)s) --> %(base_path)s',
                        locals())
