# -*- coding: utf-8 -*- äöü
# Python compatibility:
from __future__ import absolute_import

# Zope:
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

# visaplan:
from Products.unitracc.security import SecurityContext
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.tools.sequences import columns as to_columns

# Local imports:
from .utils import extract_1st_image_src


class IArticle(Interface):

    def search():
        """ """

    def feed(max_items=10):
        """
        gib Artikel fuer den RSS-Feed zurueck
        """

    def getFirstImage(brain, scaling):
        """ """

    def searchArticle():
        """ """

    def columns(*args):
        """
        Gib soviele "Spalten" von Artikeln zurück wie Argumente übergeben wurden,
        in der Regel: 2.  Jedes Argument muß eine ganze Zahl sein.
        """

    def searchArchiv():
        """ """


class Browser(BrowserView):

    implements(IArticle)

    days = 90

    def search(self, limit=0, query={}, **kwargs):
        """
        Allgemeine Suche nach Artikeln

        limit -- ?
        query -- Dict. mit Defaults (koennen ueberschrieben werden)
        kwargs -- werden abschliessend angewendet
        """
        context = self.context
        pc = getToolByName(context, 'portal_catalog')

        query['portal_type'] = 'UnitraccArticle'
        query['sort_on'] = 'effective'
        query['sort_order'] = 'reverse'
        query['effective'] = {'query': DateTime(),
                              'range': 'max'}

        if limit:
            query['sort_limit'] = limit
        query.update(kwargs)

        return pc(query)

    def feed(self, max_items=10):
        """
        gib Artikel fuer den RSS-Feed zurueck
        """
        kwargs = {'review_state': ['inherit', 'published'],
                  }
        if max_items is None:
            return self.search(**kwargs)
        else:
            return self.search(**kwargs)[:max_items]

    def searchArticle(self):
        """ """
        query = {}
        query['review_state'] = ['inherit', 'published']

        return self.search(query=query)

    def columns(self, *args):
        """
        Gib soviele "Spalten" von Artikeln zurück wie Argumente übergeben wurden,
        in der Regel: 2.  Jedes Argument muß eine ganze Zahl sein.
        """
        return to_columns(self.searchArticle(), *args)

    def searchArchiv(self):
        """ """
        context = self.context
        portal = getToolByName(context, 'portal_url').getPortalObject()

        query = {}
        query['created'] = {'query': DateTime() - self.days,
                            'range': 'max'}
        query['review_state'] = 'visible'

        with SecurityContext(context, verbose=0):
            brains = self.search(query=query)
            return brains

    def getFirstImage(self, brain, scaling):
        """
        Filtere die erste Bild-URL aus dem Seitentext

        Achtung: Es wird schlicht der Inhalt des ersten src-Attributs
                 verwendet - oder des ersten Attributs, dessen Name auf
                 'src' endet!
        """
        context = self.context
        portal = getToolByName(context, 'portal_url').getPortalObject()

        with SecurityContext(context, verbose=0):
            if brain.portal_type == 'UnitraccArticle':
                text = str(brain.getRawText)
                url = extract_1st_image_src(text, scaling)
                if url:
                    return url

        # keine enthaltenes Bild gefunden; verwende Standard-Piktogramm:
        image = context.restrictedTraverse('article_default_' + scaling + '.jpg', None)
        if image:
            return image.absolute_url()

# vim: ts=8 sts=4 sw=4 si et hls
