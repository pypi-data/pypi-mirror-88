# -*- coding: utf-8 -*- äöü
# Python compatibility:
from __future__ import absolute_import

# Zope:
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from zExceptions import NotFound

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.browsers.article.utils import extract_1st_image_src
from visaplan.plone.tools.forms import merge_qvars, tryagain_url
from visaplan.tools.sequences import columns as to_columns

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport

LOGGER, debug_active, DEBUG = getLogSupport(fn=__file__)
# Standard library:
from pprint import pformat


class INewsBrowser(Interface):

    def search():
        """ """

    def getImageUrl(brain, scaling):
        """
        Gib die URL des Vorschaubilds für die Listenansicht zurück

        Prioritätenliste:
        1. das explizite Vorschaubild (wie -> getImage)
        2. die erste im Seitentext gefundene Bild-URL
        3. das Standard-Piktogramm für News (die Zeitung; wie -> getImage)
        """

    def getImage():
        """ """

    def searchNews():
        """ """

    def columns(*args):
        """
        Gib soviele "Spalten" von Meldungen zurück wie Argumente übergeben wurden,
        in der Regel: 2.  Jedes Argument muß eine ganze Zahl sein.
        """

    def feed(max_items=10):
        """
        gib News-Objekte fuer den RSS-Feed zurueck
        """

    def searchArchiv():
        """ """


class Browser(BrowserView):

    implements(INewsBrowser)

    days = 90

    def search(self, limit=0, query=None, **kwargs):
        """
        Allgemeine Suche nach News

        limit -- ?
        query -- Dict. mit Defaults (koennen ueberschrieben werden)
        kwargs -- werden abschliessend angewendet
        """
        context = self.context
        now = DateTime()
        form = context.REQUEST.form
        pc = getToolByName(context, 'portal_catalog')
        if query is None:
            query = {}
        query.update({
            'portal_type': 'UnitraccNews',
            'effective': {'query': now,
                          'range': 'max'},
            'expires': {'query': now,
                        'range': 'min'},
            })

        queryString = form.get('SearchableText', '')
        if queryString:  # Suchbegriff angegeben
            txng = context.getBrowser('txng')
            DEBUG('search: queryString (1) = %(queryString)r', locals())
            queryString = txng.processWords(queryString)
            DEBUG('search: queryString (2.txng) = %(queryString)r', locals())

        if queryString:
            query['SearchableText'] = queryString
        else:  # kein Suchbegriff angegeben: neueste zuerst
            query['sort_on'] = 'effective'
            query['sort_order'] = 'reverse'

        if limit:
            query['sort_limit'] = limit

        query.update(kwargs)

        return pc(query)

    def searchNews(self):
        """ """
        query = {}
        query['review_state'] = ['inherit', 'published']

        return self.search(query=query)

    def columns(self, *args):
        """
        Gib soviele "Spalten" von Meldungen zurück wie Argumente übergeben wurden,
        in der Regel: 2.  Jedes Argument muß eine ganze Zahl sein.
        """
        return to_columns(self.searchNews(), *args)

    def feed(self, max_items=10):
        """
        gib News-Objekte fuer den RSS-Feed zurueck
        """
        kwargs = {'review_state': ['inherit', 'published'],
                  }
        if max_items is None:
            return self.search(**kwargs)
        else:
            return self.search(**kwargs)[:max_items]

    def searchArchiv(self):
        """ """
        context = self.context
        portal = getToolByName(context, 'portal_url').getPortalObject()

        query = {}
        query['created'] = {'query': DateTime() - self.days,
                            'range': 'max'}
        query['review_state'] = 'visible'

        sm = portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()

        brains = self.search(query=query)

        sm.setOld()

        return brains

    def getImage(self, uid=''):
        """
        Gib Bilddaten zurück;
        zur Verwendung in URLs, auch für die Listenansicht, die
        üblicherweise durch getImageUrl erzeugt werden.

        Wenn kein explizites Vorschaubild vorhanden ist, aber Bilder im
        Seitentext verwendet werden (sehr häufiger Fall), muß
        stattdessen eine andere URL verwendet werden, die von der
        Methode getImageUrl erzeugt wird.

        """
        context = self.context
        if 0 and context.portal_type != 'UnitraccNews':
            return
        portal = getToolByName(context, 'portal_url').getPortalObject()
        rc = getToolByName(context, 'reference_catalog')
        form = context.REQUEST.form
        DEBUG('Formulardaten:\n%s', pformat(form))

        sm = portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()
        try:
            DEBUG('getImage(%(self)r, %(uid)r', locals())
            if not uid:
                uid = form.get('uid')
                DEBUG('uid ist %r', uid)

            context = rc.lookupObject(uid)
            DEBUG('context ist jetzt %(context)r', locals())
            data = self._getPreviewImageData(context)
            if data is not None:
                return data

            # letzte Möglichkeit: Standard-Piktogramm
            data = context.restrictedTraverse('news_default_%(scaling)s.jpg'
                                              % form
                                              )._data
            return data
        except Exception as e:
            LOGGER.error('%(context)r->getImage(%(uid)r):', locals())
            LOGGER.exception(e)
        finally:
            sm.setOld()

    def getImageUrl(self, brain, scaling):
        """
        Gib die URL des Vorschaubilds für die Listenansicht zurück

        Prioritätenliste:
        1. das explizite Vorschaubild (wie -> getImage)
        2. die erste im Seitentext gefundene Bild-URL
        3. das Standard-Piktogramm für News (die Zeitung; wie -> getImage)
        """
        if brain.portal_type != 'UnitraccNews':
            return
        DEBUG('getImageUrl(%(brain)r, %(scaling)r)', locals())
        context = self.context
        context.REQUEST.form['scaling'] = scaling
        portal = getToolByName(context, 'portal_url').getPortalObject()
        rc = getToolByName(context, 'reference_catalog')
        uid = brain.UID
        o = rc.lookupObject(uid)

        sm = portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()
        try:
            # explizites Vorschaubild vorhanden?
            if o.hasImage():
                return merge_qvars('@@news/getImage',
                                   [('scaling', scaling),
                                    ('uid', uid),
                                    ])
            text = str(brain.getRawText)
            url = extract_1st_image_src(text, scaling)
            if url:
                return url

            # kein Bild im Text gefunden; verwende Standard-Piktogramm:
            image = context.restrictedTraverse('news_default_' + scaling + '.jpg', None)
            if image:
                return image.absolute_url()
        except Exception as e:
            LOGGER.error('%(context)r->getImageUrl(%(brain)r, %(scaling)r):', locals())
            LOGGER.exception(e)
        finally:
            sm.setOld()

    def _getPreviewImageData(self, o):
        """
        Gib die Bilddaten des konfigurierten Vorschaubilds zurück,
        aber *nicht* die des als letzte Möglichkeit zu verwendenden
        Standard-Piktogramms
        """
        scaling = o.getBrowser('scaling')
        data = scaling.get()
        if data:
            DEBUG('Ok: explizites Vorschaubild gefunden')
            # explizites Vorschaubild gefunden
            return data or None


# vim: ts=8 sts=4 sw=4 si et hls
