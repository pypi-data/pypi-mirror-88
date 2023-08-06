# Python compatibility:
from __future__ import absolute_import

# Standard library:
import os
from os import popen, sep
from os.path import exists, getmtime, getsize
from time import gmtime

# Zope:
from App.Common import rfc1123_date
from App.config import getConfiguration
from DateTime import DateTime
from ZPublisher.Iterators import filestream_iterator

# 3rd party:
import PIL.Image
from cStringIO import StringIO

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements


class IFlvPreview(Interface):

    pass


class Browser(BrowserView):

    implements(IFlvPreview)

    COMMAND = 'ffmpeg -y -i %(input)s -f mjpeg -ss %(second)s -vframes 1 -s %(width)sx%(height)s -an %(output)s'
    cache_duration = 3600
    configStorageKey = 'flvpreview'

    def _storage_path(self):
        """ """
        return getConfiguration().product_config.get('flv', {})['flv_dir'] + os.sep

    def __call__(self):
        """ """
        context = self.context

        if hasattr(context, 'getContentType') and context.getContentType().startswith('video'):
            form = context.REQUEST.form

            storage_path = self._storage_path() + context.UID() + '_flash_file'
            flvinfo = context.getAdapter('flvinfo')

            query = flvinfo(context.UID())
            if int(query['width']):
                query['input'] = storage_path
                query['second'] = '4'
                query['width'] = str(int(query['width']))
                query['height'] = str(int(query['height']))
                query['output'] = storage_path + '_' + query['width'] + 'x' + query['height']

                requestedOutputPath = storage_path + '_' + form.get('width', query['width']) + 'x' + form.get('height', query['height'])

                if not exists(query['output']):
                    popen(self.COMMAND % query)

                if not exists(requestedOutputPath):
                    original_file = StringIO(open(query['output'], 'rb').read())
                    image = PIL.Image.open(original_file)
                    image.thumbnail((int(form.get('width', 0)), int(form.get('height', 0))), PIL.Image.ANTIALIAS)
                    thumbnail_file = StringIO()
                    image.save(thumbnail_file, 'JPEG', quality=100)
                    open(requestedOutputPath, 'wb').write(thumbnail_file.getvalue())
                    original_file.close()
                    thumbnail_file.close()

                if exists(requestedOutputPath):
                    tuple_ = gmtime(getmtime(query['output']))
                    response = context.REQUEST.RESPONSE
                    modified = DateTime('%s/%s/%s/ %s:%s' % (tuple_[0], tuple_[1], tuple_[2], tuple_[3], tuple_[4]))
                    response.setHeader('Last-Modified', (modified).toZone('GMT').rfc822().split('+')[0] + 'GMT')
                    response.setHeader('Expires', rfc1123_date((DateTime() + self.cache_duration).timeTime()))
                    response.setHeader('Cache-Control', 'max-age=%d' % int(self.cache_duration * 24))
                    response.setHeader('Accept-Ranges', 'bytes')
                    response.setHeader('Content-Type', 'image/jpeg')
                    response.setHeader('Content-Length', getsize(requestedOutputPath))
                    response.setHeader(
                    'Content-Disposition',
                    'inline; filename="%s.jpg"' % context.getId()
                    )
                    return filestream_iterator(requestedOutputPath, 'rb')

    def __bobo_traverse__(self, REQUEST, scaling):
        """redirect to call"""
        context = self.context
        width, height = scaling.split('x')
        form = context.REQUEST.form
        form.update({'width': width,
                     'height': height})
        return self()
