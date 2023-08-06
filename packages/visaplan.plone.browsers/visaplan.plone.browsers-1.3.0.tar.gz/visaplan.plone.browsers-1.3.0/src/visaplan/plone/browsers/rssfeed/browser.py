# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import, print_function

# Zope:
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.context import make_timeFormatter, parents


class IRssFeed(Interface):

    def get():
        """ """


class Browser(BrowserView):

    implements(IRssFeed)

    config_storage_key = 'rssfeed'

    def _get_config(self):
        """ """
        context = self.context
        settings = context.getBrowser('settings')
        portal = getToolByName(context, 'portal_url').getPortalObject()
        feeds = {}
        for url in settings.get(self.config_storage_key, {}).get('mapping', '').split('\r\n'):
            if len(url.split('; ')) == 3:
                recursive, uid, url = url.split('; ')
                dict_ = {}
                dict_['recursive'] = (recursive == '1' and True or False)
                dict_['uid'] = uid
                if not url.startswith('http://'):
                    dict_['url'] = portal.absolute_url() + '/' + url
                feeds[dict_['uid']] = dict_
        return feeds

    def get(self):

        context = self.context
        if hasattr(context, 'getCanonical'):
            context = context.getCanonical()

        dict_ = self._get_config()
        for object_ in parents(context)[:-1]:
            if hasattr(object_, 'UID'):
                if hasattr(object_, 'getCanonical'):
                    object_ = object_.getCanonical()
                if object_.UID() in dict_:
                    if dict_[object_.UID()]['recursive']:
                        return dict_[object_.UID()]
                    else:
                        if object_.UID() == context.UID():
                            return dict_[object_.UID()]
        return {}

    def debug(self):
        """
        fuer Entwicklungszwecke: gib Informationen zur Konsole aus
        """

        def anames(o):
            return [a for a in dir(o)
                    if not a.startswith('_')]
        print('*' * 79)
        print('%s:' % __file__)
        print('Klasse %s' % (self.__class__.__name__))
        print('Attribute: %s' % (anames(self),))
        print('self.context: %s' % (self.context,))
        try:
            gc = context.getContext
        except AttributeError as e:
            print('Attributfehler: %s' % str(e))
        else:
            context = gc()
        print('Kontext:')
        print('Attribute: %s' % (anames(context),))
        print('*' * 79)

    def setHeader(self, context=None):
        """
        Setze Content-Type-Header
        """
        print('Setze Header fuer RSS ...')
        if context is None:
            context = self.getContext()
        request = context.request
        encoding = context.plone_utils.getSiteEncoding()
        request.RESPONSE.setHeader('Content-Type',
                                   'text/xml;charset=' + context)
        print('Header fuer RSS ... OK')

    def html4time(self, secs):
        return DateTime(secs).HTML4()

    def getInfo(self, context=None):
        """
        Informationen und Funktionen zur Verwendung in Templates
        """
        if context is None:
            context = self.context

        if 1:
            try:
                portal_url = context.portal_url
            except Exception as e:
                print('E:%s' % str(e))
                portal_url = 'http://www.unitracc.de'
        else:
            portal_url = 'http://www.unitracc.de'

        return {'portal_url': portal_url,  # wird schon nicht mehr benoetigt
                'totime': make_timeFormatter(context),
                'html4time': self.html4time,
                }

    def getOInfo(self, o):
        """
        nur fuer Entwicklungszwecke: Objekt-Info
        """

        def show(a):
            blacklist_heads = ('_', 'set', 'manage', 'add', 'wl_')
            blacklist_tails = ['__',
                               ]
            for s in blacklist_heads:
                if a.startswith(s):
                    return False
            for s in blacklist_tails:
                if a.endswith(s):
                    return False
            return True

        res = []
        res.append(repr(o) + ':')
        res.extend([a for a in dir(o)
                    if show(a)])
        return '\n'.join(res)

    def getAuthor(self, o):
        """
        Extrahiere die Autoreninformation, wie sie im Feed erscheinen soll
        """
        res = {}
        fullname = []
        fullname.append(o.getContactAcademicTitle())
        fullname.append(o.getContactFirstname())
        fullname.append(o.getContactLastname())
        res['name'] = ' '.join([stripped
                                for stripped in [v.strip() for v in fullname]
                                if stripped])
        return res
        # vorerst keine Mail-Information:
        email = o.getContactEmail
        print('%(o)r -> %(res)s' % locals())

    def getNews(self, max_items):
        """
        Gib die News gemaess dem Browser 'news' zurueck
        """
        context = self.context
        news = context.getBrowser('news')
        return news.feed(max_items)

    def getEvents(self, max_items):
        """
        Gib die Termine gemaess dem Browser 'events' zurueck
        """
        context = self.context
        events = context.getBrowser('event')
        return events.feed(max_items)

    def getArticles(self, max_items):
        """
        Gib die Artikel gemaess dem Browser 'article' zurueck
        """
        context = self.context
        articles = context.getBrowser('article')
        return articles.feed(max_items)

# vim: ts=8 sts=4 sw=4 si et hls
