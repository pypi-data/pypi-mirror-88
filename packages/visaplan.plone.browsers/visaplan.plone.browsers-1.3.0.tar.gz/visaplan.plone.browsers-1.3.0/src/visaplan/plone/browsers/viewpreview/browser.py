# -*- coding: utf-8 -*- äöü
"""
unitracc@@viewpreview: Vorschaubilder verwalten
"""
# Python compatibility:
from __future__ import absolute_import

from six import string_types as six_string_types
from six.moves._thread import start_new_thread

# Standard library:
from collections import defaultdict
from os import listdir, sep, unlink
from os.path import exists, getsize, join

# Zope:
from AccessControl import Unauthorized
from App.config import getConfiguration
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from ZPublisher.Iterators import filestream_iterator

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements

# Local imports:
from .utils import get_dir, get_filename, make_pushfunc

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport

logger, debug_active, DEBUG = getLogSupport()

pushfunc = make_pushfunc(logger=logger)


class IViewPreview(Interface):

    def get():
        """
        Gib das Vorschaubild für den aktuellen Kontext zurück;
        wenn noch nicht vorhanden, rufe push auf (und gib implizit None zurück)
        """

    def push():
        """
        Fordere ein neues Vorschaubild an
        """

    def html():
        """
        Gib den HTML-Text der Präsentationsansicht der Seite mit der
        angegebenen <uid> zurück;
        ersetze alle Vorkommen von /resolve[uU]id/
        durch Verweise auf die --> getData-Methode.
        """

    def save():
        """
        Nimm die Bilddaten <file> für das Objekt mit der UID <token> entgegen
        und speichere die Bildatei.

        Diese Methode wird vom Bilder-Server aufgerufen!
        """

    def getData():
        """
        Gib "das Bild" für die im path-Argument übergebene UID zurück,
        ggf. unter Verwendung des scaling-Browsers
        """

    def update():
        """
        Lösche das Vorschaubild für den Kontext
        und veranlasse die Generierung einer neuen Version.
        """

    def cleanup():
        """
        Räume das Verzeichnis der Vorschaubilder auf:
        Iteriere über alle dort gespeicherten Bilder und lösche alle, deren UID
        (aus dem Dateinamen ermittelt) im Katalog keinen Treffer zeitigt.
        """


class Browser(BrowserView):

    implements(IViewPreview)

    def _storage_path(self):
        """
        Nicht mehr verwendet; siehe --> .utils.get_dir()
        """
        return getConfiguration().product_config.get('viewpreview', {})['viewpreview_dir'] + sep

    def push(self):
        """
        Fordere ein neues Vorschaubild an
        """
        context = self.context
        uid = context.UID()
        tid = start_new_thread(pushfunc, (),
                               {'uid': uid,
                                'context': context,
                                'logger': logger,
                                })
        logger.info('push(): uid=%(uid)r, thread: %(tid)r', locals())

    def save(self):
        """
        Nimm die Bilddaten <file> für das Objekt mit der UID <token> entgegen
        und speichere die Bildatei.

        Diese Methode wird vom Bilder-Server aufgerufen!
        """

        #if context.REQUEST['HTTP_X_FORWARDED_FOR']!='78.47.151.91':
        #    return ''
        context = self.context
        OK = False
        portal = getToolByName(context, 'portal_url').getPortalObject()
        sm = portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()
        try:
            form = context.REQUEST.form

            file = form.get('file', '')
            uid = form.get('token', '')
            logger.info('Receiving preview image for UID %(uid)r', locals())
            logger.info('file=%(file)r', locals())
            if not isinstance(file, six_string_types):
                data = file.read()
                image = self.createImage()
                field = image.getField('image')
                io = field.scale(data=data, w=200, h=150)[0]
                scaledData = io.read()
                io.seek(0)
                path = get_filename(uid)
                open(path, 'wb').write(scaledData)
                OK = True
                logger('Preview image for %(uid)r written to %(path)s',
                        locals())
            else:
                logger.warn('file %s: currently ignored', type(file))
        except OSError as e:
            logger.error('Error receiving preview image for UID %(uid)r: %(e)s',
                         locals())
            logger.exception()
        finally:
            sm.setOld()
            if OK:
                return 'OK'
            else:  # von pdfserver4.tcis.de akzeptierter Wert unsicher:
                return 'ERROR'

    def update(self):
        """
        Lösche das Vorschaubild für den Kontext
        und veranlasse die Generierung einer neuen Version.
        """
        context = self.context

        checkperm = getToolByName(context, 'portal_membership').checkPermission
        if not checkperm('Modify portal content', context):
            raise Unauthorized

        uid = context.UID()
        path = get_filename(uid)
        if exists(path):
            unlink(path)
            logger.info('update: deleted %(path)s', locals())

        self.push()

    def get(self):
        """
        Gib das Vorschaubild für den aktuellen Kontext zurück
        """
        context = self.context
        uid = context.UID()
        path = get_filename(uid)
        if not exists(path):
            self.push()
        if exists(path):
            RESPONSE = context.REQUEST.RESPONSE
            setHeader = RESPONSE.setHeader
            setHeader('Content-Type', 'image/jpg')
            setHeader('Content-Length', getsize(path))
            setHeader('Last-Modified', (context.modified()).toZone('GMT').rfc822().split('+')[0] + 'GMT')
            setHeader(
                'Content-Disposition',
                'inline; filename="%s"' % context.getId() + '.jpg'
                )
            return filestream_iterator(path, mode='rb')

    def createImage(self):
        """
        Aufgerufen von --> save()
        """
        context = self.context

        portal = getToolByName(context, 'portal_url').getPortalObject()

        # TODO: getToolByName verwenden?
        return portal.restrictedTraverse('portal_factory/UnitraccImage/neu')

    def html(self):
        """
        Gib den HTML-Text der Präsentationsansicht der Seite mit der
        angegebenen <uid> zurück;
        ersetze alle Vorkommen von /resolve[uU]id/
        durch Verweise auf die --> getData-Methode.
        """
        context = self.context
        #if context.REQUEST['HTTP_X_FORWARDED_FOR']!='78.47.151.91':
        #    return ''

        form = context.REQUEST.form
        portal = getToolByName(context, 'portal_url').getPortalObject()
        rc = getToolByName(context, 'reference_catalog')

        uid = form.get('uid', None)
        if not uid:
            logger.error('html: uid is %(uid)r', locals())

        html = ''
        sm = portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()
        try:

            object_ = rc.lookupObject(uid)
            if object_:
                html = object_.restrictedTraverse('ppt_preview')()
                purl = portal.absolute_url()
                subst = purl + '/@@viewpreview/getData?path='
                # TODO: HTML-Parser verwenden;
                #       Links sicherer erkennen
                html = html.replace('./resolveUid/', subst)
                html = html.replace('./resolveuid/', subst)
                html = html.replace('./@@resolveuid/', subst)
            else:
                logger.error('html: no object found for uid %(uid)r', locals())

        finally:
            sm.setOld()
            return html

    def cleanup(self):
        """
        Räume das Verzeichnis der Vorschaubilder auf:
        Iteriere über alle dort gespeicherten Bilder und lösche alle, deren UID
        (aus dem Dateinamen ermittelt) im Katalog keinen Treffer zeitigt.
        """
        context = self.context

        checkperm = getToolByName(context, 'portal_membership').checkPermission
        if not checkperm('Manage portal', context):
            raise Unauthorized

        storagePath = get_dir()
        logger.info('cleanup for storagePath %(storagePath)s ...', locals())
        cnt = defaultdict(int)
        catalog = getToolByName(context, 'portal_catalog')._catalog
        # TODO: ausführen in Thread, mit os.chdir?
        for fileName in listdir(storagePath):
            try:
                if fileName.endswith('_ppt'):
                    cnt['ppt'] += 1
                    uid = fileName.split('_')[0]
                    if not catalog(UID=uid):
                        cnt['zombie'] += 1
                        ffn = join(storagePath, fileName)
                        unlink(ffn)
                        cnt['deleted'] += 1
                else:
                    cnt['no-ppt'] += 1
            except OSError as e:
                logger.error('error %(e)r deleting file %(filename)s', locals())
                cnt['errors'] += 1
        for key in ('ppt', 'no-ppt',
                    'zombie', 'deleted', 'errors',
                    ):
            logger.info('cleanup: %4d %s', cnt[key], key)
        if not cnt:
            logger.info('cleanup: nothing to do')

    def getData(self):
        """
        Gib "das Bild" für die im path-Argument übergebene UID zurück,
        ggf. unter Verwendung des scaling-Browsers
        """
        context = self.context
        portal = getToolByName(context, 'portal_url').getPortalObject()
        rc = getToolByName(context, 'reference_catalog')
        sm = portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()
        try:
            form = context.REQUEST.form
            path = form.get('path', '')

            splittedPath = path.split('/')

            uid = splittedPath
            DEBUG('uid is %(uid)r', locals())

            object_ = rc.lookupObject(uid)

            if path.find('scaling') != -1:
                DEBUG('%(path)r --> scaling:', locals())
                val = path.split('?')[1].split('=')[1]
                DEBUG('value is %(val)r', locals())
                form.update({'scaling': val})
                return object_.getBrowser('scaling').get()
            else:
                return object_.getImage()
        finally:
            sm.setOld()
