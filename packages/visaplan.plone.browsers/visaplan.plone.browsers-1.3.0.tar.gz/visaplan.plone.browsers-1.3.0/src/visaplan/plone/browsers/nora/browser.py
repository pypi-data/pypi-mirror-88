# -*- coding: utf-8 -*- äöü
# Python compatibility:
from __future__ import absolute_import

# Standard library:
from pprint import pformat

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
import pdb
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import log_or_trace, pp, trace_this

LOGGER, debug_active, DEBUG = getLogSupport(fn=__file__,
                                            defaultFromDevMode=0)

lot_kwargs = {
    'debug_level': debug_active,
    'logger': LOGGER,
    'trace': 0,
    }


class INewsOrArticlesBrowser(Interface):

    def search():
        """
        Suche nach News und Artikeln (per Vorgabe: max. 12)
        """

    def search_all():
        """
        Suche alle News und Artikel
        """

    def search_others():
        """
        Gib einige News und Artikel zurück, aber nicht den aktuell angezeigten
        """

    def search_siblings(**kwargs):
        """
        Finde die "Geschwister" des aktuellen Kontexts
        """

    # ------------- [ Suche nach weiteren Inhaltstypen ... [
    def search_images(**kwargs):
        """
        Suche nach Bildern
        """

    def search_animations(**kwargs):
        """
        Suche nach Bildern
        """

    def search_videos(**kwargs):
        """
        Suche nach Bildern
        """
    # ------------- ] ... Suche nach weiteren Inhaltstypen ]

    def search_a():
        """
        Für Entwicklungszwecke:
        Suche *nur* nach Artikeln (von denen es weniger gibt)
        """

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


class Browser(BrowserView):

    implements(INewsOrArticlesBrowser)

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
        DEBUG('getImageUrl(%(brain)r, %(scaling)r)', locals())
        context = self.context
        context.REQUEST.form['scaling'] = scaling  # TH: warum in Formulardaten?
        portal = getToolByName(context, 'portal_url').getPortalObject()
        rc = getToolByName(context, 'reference_catalog')
        uid = brain.UID
        # pp(portal_type=brain.portal_type, hasImage=brain.hasImage)
        if 0 and brain.portal_type == 'UnitraccArticle':
            pdb.set_trace()

        # explizites Vorschaubild vorhanden?
        if brain.hasImage:
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

    def _query(self, context, **kwargs):
        """
        Erzeuge die Suchargumente für --> search
        """
        query = {
            'portal_type': ['UnitraccNews',
                            'UnitraccArticle',
                            ],
            'getExcludeFromSearch': False,
            'sort_on': 'effective',
            'sort_order': 'reverse',
            'effective': {'query': DateTime(),
                          'range': 'max',
                          },
            'review_state': ['visible', 'inherit',
                             'published', 'restricted',
                             ],
            }

        form = context.REQUEST.form

        queryString = form.get('SearchableText', '')
        if queryString:
            DEBUG('search: queryString (1) = %(queryString)r', locals())
            txng = context.getBrowser('txng')
            queryString = txng.processWords(queryString).strip()
            DEBUG('search: queryString (2.txng) = %(queryString)r', locals())

        if queryString:
            queryString = '*' + queryString + '*'
            query['SearchableText'] = queryString

        if 'getCustomSearch' in form:
            query['getCustomSearch'] = form['getCustomSearch']

        # Noch keine Behandlung etwaiger Doppelangaben:
        if kwargs:
            query.update(kwargs)
        return query

    def search_all(self):
        """
        @@nora.search_all: Suche alle News und Artikel
        """
        return self.search(search_limit=None)

    def search(self, **kwargs):
        """
        @@nora.search: Suche News und Artikel

        Die Suche ergibt üblicherweise zu wenige Artikel (bzw. gar
        keine, wegen der häufigeren und i.d.R. neueren News);
        dieses Verhalten ist bekannt und beabsichtigt.

        Schlüsselwort-Argumente:

        as_system -- wenn True, wird per securitymanager als system-Benutzer gesucht

        Weitere siehe --> _search bzw. and Katalogsuche weitergereicht.
        """
        context = self.context
        if not kwargs.pop('as_system', False):
            return self._search(context, **kwargs)
        portal = getToolByName(context, 'portal_url').getPortalObject()

        sm = portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()
        try:
            return self._search(context, **kwargs)
        finally:
            sm.setOld()

    def _search(self, context, **kwargs):

        if 'search_limit' in kwargs:
            limit = kwargs['search_limit']
            if limit is None:
                del kwargs['search_limit']
            else:
                kwargs['search_limit'] = limit = int(kwargs['search_limit'])
        else:
            kwargs['search_limit'] = limit = 12
        skip_uid = kwargs.pop('skip_uid', None)
        if skip_uid is not None and limit is not None:
            kwargs['search_limit'] += 1
        # balanced_list/minimum nicht mehr verwendet:
        if 'minimum' in kwargs:
            LOGGER.error('_search: "minimum" argument ignored (%(kwargs)s)', locals())
            del kwargs['minimum']

        pc = getToolByName(context, 'portal_catalog')
        query = self._query(context, **kwargs)
        tutti = pc(query)
        if skip_uid is None:
            if limit is None:
                return tutti
            return tutti[:limit]
        elif limit is None:
            return [brain
                    for brain in tutti
                    if brain.UID != skip_uid
                    ]
        else:
            return [brain
                    for brain in tutti
                    if brain.UID != skip_uid
                    ][:limit]
        # nunmehr toter Code:
        query['portal_type'] = 'UnitraccArticle'
        articles = pc(query)

    def search_a(self):
        """
        Für Entwicklungszwecke:
        Suche *nur* nach Artikeln (von denen es weniger gibt)
        """
        return self.search(portal_type='UnitraccArticle')

    @log_or_trace(**lot_kwargs)
    def search_others(self):
        """
        Gib einige News und Artikel zurück, aber nicht den aktuell angezeigten
        """
        kwargs = {}
        context = self.context
        uid = context._getUID()
        if uid:
            kwargs['skip_uid'] = uid
        return self._search(context, **kwargs)

    def search_siblings(self, **kwargs):
        """
        Finde die "Geschwister" des aktuellen Kontexts
        """
        context = self.context
        if 'skip_uid' not in kwargs:
            uid = context._getUID()
            if uid:
                kwargs['skip_uid'] = uid
        elif not kwargs['skip_uid']:
            del kwargs['skip_uid']
        if 'portal_type' not in kwargs:
            pt = context.portal_type
            if pt.startswith('Unitracc'):
                kwargs['portal_type'] = pt
        return self._search(context, **kwargs)

    # ------------- [ Suche nach weiteren Inhaltstypen ... [
    def search_images(self, **kwargs):
        """
        Suche nach Bildern
        """
        kwargs['portal_type'] = ['UnitraccImage',
                                 # 'Image',
                                 ]
        if 'hasCode' not in kwargs:
            kwargs['hasCode'] = 1
        elif kwargs['hasCode'] is None:
            del kwargs['hasCode']
        else:
            kwargs['hasCode'] = int(kwargs['hasCode'])
        # TODO: Portal-ID ermitteln und verwenden
        kwargs['path'] = '/unitracc/mediathek/structure'
        return self.search(**kwargs)

    def search_animations(self, **kwargs):
        """
        Suche nach Bildern
        """
        kwargs['portal_type'] = ['UnitraccAnimation',
                                 ]
        return self.search(**kwargs)

    def search_videos(self, **kwargs):
        """
        Suche nach Bildern
        """
        kwargs['portal_type'] = ['UnitraccVideo',
                                 ]
        return self.search(**kwargs)
    # ------------- ] ... Suche nach weiteren Inhaltstypen ]


# vim: ts=8 sts=4 sw=4 si et hls
