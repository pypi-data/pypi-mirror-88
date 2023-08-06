# -*- coding: utf-8 -*- äöü

# Python compatibility:
from __future__ import absolute_import

# Standard library:
from collections import defaultdict
from json import dumps as json_dumps
from random import choice, randrange, shuffle
from time import time
from xml.etree.cElementTree import Element, SubElement
from xml.etree.cElementTree import tostring as etree_tostring

# Zope:
from Products.CMFCore.utils import getToolByName

# Plone:
from plone.memoize import ram

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.base.permissions import Manage_Ads as PERM_MANAGE
from visaplan.plone.tools.cfg import get_raw_config
from visaplan.plone.tools.context import getActiveLanguage
from visaplan.tools.dicts import getOption
from visaplan.tools.minifuncs import NoneOrInt, gimmeConst__factory, makeBool
from visaplan.tools.sequences import matrixify, next_of

# Local imports:
from .util import localurl

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import log_result

logger, debug_active, DEBUG = getLogSupport(fn=__file__)

# ------------------------------------------------- [ Daten ... [
#  ----------------------------------- [ Konfiguration ... [
CONFIG = get_raw_config(fn=__file__, defaults={
    'enabled': True,
    'slot-size': 4,
    'cache-timeout': 3600,
    'reload-timeout': 600,  # Neuladen nach 600 Sekunden (10min)
    })

# Ist die Werbung aktiviert?
ADS_ENABLED = getOption(CONFIG, 'enabled', default='true', factory=makeBool)
ADS_DISABLED = not ADS_ENABLED
# für je <SLOT_SIZE> angefangene Werbebuchungen wird eine Graphik ausgeben:
SLOT_SIZE = NoneOrInt(CONFIG['slot-size'])
if SLOT_SIZE is None:
    SLOT_SIZE = 4
# Timeout für Cache in Sekunden:
CACHE_TIMEOUT = NoneOrInt(CONFIG['cache-timeout'])
if CACHE_TIMEOUT is None:
    logger.info('Cache-Timeout:            %r', CACHE_TIMEOUT)
    CACHE_TIMEOUT_MS = None
else:
    logger.info('Cache-Timeout:            %d Sekunden', CACHE_TIMEOUT)
    CACHE_TIMEOUT_MS = 1000 * CACHE_TIMEOUT
logger.info('Max. Belegungen pro Slot: %d', SLOT_SIZE)
# Automatisches Neuladen per Javascript:
RELOAD_TIMEOUT_S = NoneOrInt(CONFIG['reload-timeout']) or 600
logger.info('Timeout zum Neuladen:     %d Sekunden', RELOAD_TIMEOUT_S)
assert RELOAD_TIMEOUT_S > 0
# Javascript verwendet Millisekunden:
RELOAD_TIMEOUT_MS = 1000 * RELOAD_TIMEOUT_S

_alt_text = CONFIG.get('alt-text', '')
ALT_TEXT = defaultdict(gimmeConst__factory(_alt_text))
ALT_TEXT.update({
    'de': 'einen Moment bitte ...',
    'en': 'one moment please ...',
    })
#  ----------------------------------- ] ... Konfiguration ]
# ------------------------------------------------- ] ... Daten ]


class IAdvertisement(Interface):

    def is_enabled():
        """
        Ist Werbung auf dieser Site generell aktiviert?
        """

    def canAdd():
        """ """

    def getAdvertiselementRightOne():
        """ """

    def getAdvertiselementRightTwo():
        """ """

    def getAdvertiselementSearch1():
        """ """

    def getAdvertiselementSearchBottom():
        """ """

    def has_advertising():
        """
        Gibt es in dieser Unitracc-Instanz Werbung?
        """

    def get_ads_json():
        """
        Gib die Werbungs-Information im JSON-Format zurück
        """

    def get_ads_html(relationship, lang=None, limit=None):
        """
        Gib die Werbungs-Information als HTML-Code zurück:
        - img-Element mit zufällig ausgewählter Werbung
        - script-Element, das die automatische Wechseln der Bilder
          (RELOAD_TIMEOUT_MS) und das automatische Nachladen der Konfiguration
          (CACHE_TIMEOUT * 1000) anstößt
        """


def make_cachefunc():
    quot = CACHE_TIMEOUT
    def cachekey_1(method, self, relationship, recurse=False):
        context = self.context
        return (getActiveLanguage(context),
                context.UID(),  # TH: warum die UID?!
                relationship,
                bool(recurse),
                )
    def cachekey_2(method, self, relationship, recurse=False):
        context = self.context
        return (getActiveLanguage(context),
                int(time()) // quot % 32000,
                relationship,
                bool(recurse),
                )

    if quot is None:
        f = cachekey_1
    else:
        assert isinstance(quot, int) and quot > 1
        f = cachekey_2

    if not debug_active:
        return f

    return log_result(logger=logger)(f)


cache_key = make_cachefunc()


def make_basekeyfunc(key, quot=CACHE_TIMEOUT):
    """
    Erzeuge eine cachekey-Funktion für den reinen @@stage.get-Aufruf;
    es wird hier noch keinerlei zufällige Transformation und/oder Auswahl vorgenommen!
    """
    if quot is None:
        quot = 3600  # eine Stunde
    assert isinstance(quot, int) and quot > 1

    def basekey(method, self, relationship, lang=None, *args):
        if lang is None:
            lang = getActiveLanguage(self.context)
        return (lang,
                key,
                int(time()) // quot % 32000,
                relationship,
                )

    if not debug_active:
        return basekey

    return log_result(logger=logger)(basekey)


def make_newkeyfunc(quot=CACHE_TIMEOUT):
    """
    Erzeuge eine cachekey-Funktion, die das lang-Argument ggf. selbst ermittelt
    """


def random_subset(seq):
    """
    Ersatz für die Methode .random
    """
    liz = list(seq)
    shuffle(liz)
    return [sublist[0]
            for sublist in matrixify(liz, SLOT_SIZE)]


class Browser(BrowserView):

    implements(IAdvertisement)

    def is_enabled(self):
        """
        Ist Werbung auf dieser Site generell aktiviert?
        """
        global ADS_ENABLED
        return ADS_ENABLED

    def canAdd(self):
        """
        Kann
        - der angemeldete User
        - hier
        Werbung hinzufügen?
        """
        context = self.context
        # wie --> has_advertising:
        if not context.getBrowser('unitraccfeature').has_advertising():
            return False
        if not self.configure_here(context):
            return False
        return getToolByName(context, 'portal_membership').checkPermission(PERM_MANAGE, context)

    def getAdvertiselementAboveContent(self):
        """
        Werbebanner quer ueber dem Inhalt
        """
        objects = self.getCached('advertisement-content', True)
        return random_subset(objects)

    def getAdvertiselementRightOne(self):
        """
        Werbebanner rechts oben (ggf. mehrere)
        """
        objects = self.getCached('advertisement-right-one', True)
        return random_subset(objects)

    def getAdvertiselementRightTwo(self):
        """
        Werbebanner rechts darunter (Skyscraper) - nur eins!
        """
        objects = self.getCached('advertisement-right-two', True)
        if objects:
            return [choice(objects)]
        return []

    def getAdvertiselementSearch1(self):
        objects = self.getCached('advertisement-search-1', True)
        return objects

    def getAdvertiselementSearchBottom(self):
        objects = self.getCached('advertisement-search-bottom', True)
        return objects

    def configure_here(self, context=None):
        """
        Soll die Werbung hier konfiguriert werden?
        """
        portal_url = getToolByName(self.context, "portal_url")
        if context is None:
            context = self.context
        portal_url = context.portal_url()
        my_url = self.context.absolute_url()
        return my_url == portal_url

    @ram.cache(make_basekeyfunc('base'))
    def get_ads_from_stage(self, relationship, lang=None):
        """
        Lies die gebuchte Werbung der gegebenen Relation
        (ohne jegliche zufällige Verwürfelung oder Auswahl)
        """
        portal_url = getToolByName(self.context, "portal_url")
        portal = portal_url.getPortalObject()
        secs = time() % 10000
        DEBUG('get_ads_from_stage(%(relationship)r) at ...%(secs)4.2f', locals())
        return [{'link2url': object_.getLocation(),
                 'img_src': localurl(object_),
                 }
                for object_
                in portal.getBrowser('stage').get(relationship,
                                                  recurse=False)
                ]

    @ram.cache(make_basekeyfunc('shuffled'))
    def get_ads_data(self, relationship, lang=None, limit=None):
        """
        Gib Daten für die gebuchte Werbung der gegebenen Relation zurück;
        ein dict mit den Schlüsseln:

        relationship -- der Schlüssel, z. B. 'advertisement-right-one'
        number -- die Anzahl der gleichzeitig auszugebenden Werbungsgraphiken
                  (0 <= number <= limit;  wenn limit == None,
                  aus SLOT_SIZE und der Anzahl der Buchungen ermittelt)
        ads -- die Liste *aller* gebuchten Werbungen für diese Relation
        index -- der Index der ersten zufällig ausgewählten Werbung
                 (None, wenn number == 0)

        Argumente:
        lang -- die Sprache kann vorab ermittelt und übergeben werden
        limit -- z. B. 1 für den Skyscraper

        """
        if lang is None:
            lang = getActiveLanguage(self.context)

        ads = self.get_ads_from_stage(relationship, lang)
        if not ads:
            return {'ads': [],
                    'adslength': 0,
                    'number': 0,
                    'lang': lang,
                    'alt': ALT_TEXT[lang],
                    'relationship': relationship,
                    'reload_ms': RELOAD_TIMEOUT_MS,
                    'lifetime_ms': CACHE_TIMEOUT_MS,
                    'index': None,
                    }
        # Jedenfalls zu beachtende Obergrenze:
        number, rest = divmod(len(ads), SLOT_SIZE)
        if rest:
            number += 1
        if limit is not None and number > limit:
            assert isinstance(limit, int) and limit >= 0, \
                    'limit >= 0 erwartet: %(limit)r' % locals()
            number = limit

        adslength = len(ads)
        return {'ads': ads,
                'adslength': adslength,
                'number': number,
                'lang': lang,
                'alt': ALT_TEXT[lang],
                'relationship': relationship,
                'reload_ms': RELOAD_TIMEOUT_MS,
                'lifetime_ms': CACHE_TIMEOUT_MS,
                'index': None if not number
                         else (0 if adslength == 1
                               else randrange(0, adslength)
                               ),
                }

    @ram.cache(make_basekeyfunc('json'))
    def _get_ads_json(self, relationship, lang=None, limit=None):
        return json_dumps(self.get_ads_data(relationship, lang, limit))

    def get_ads_json(self):
        """
        Gib die Werbungs-Information im JSON-Format zurück

        Die folgenden Informationen sind dem Client aus dem HTML-Code
        (--> get_ads_html) bekannt und werden daher stets übermittelt:

        relation -- die Relation, z. B. 'advertisement-right-one'
        lang -- der Sprachcode

        Das folgende ist optional (und wird bislang noch nicht verwendet):

        limit -- um die Anzahl speziell zu begrenzen, z. B. für den Skyscraper
                 ('advertisement-right-two')
        """
        request = self.context.REQUEST
        form = request.form
        relationship = form['relation']
        lang = form['lang']
        limit = form.get('limit', None)
        if limit is not None:
            limit = int(limit)
        request.RESPONSE.setHeader(
                'Content-type', 'application/json; charset=utf-8')
        return self._get_ads_json(relationship, lang, limit)

    def get_ads_html(self, relationship, lang=None, limit=None):
        """
        Gib die Werbungs-Information als HTML-Code zurück:
        - img-Element mit zufällig ausgewählter Werbung
        - script-Element, das die automatische Wechseln der Bilder
          (RELOAD_TIMEOUT_MS) und das automatische Nachladen der Konfiguration
          (CACHE_TIMEOUT * 1000) anstößt
        """
        if ADS_DISABLED:
            return '<!-- ads disabled -->'
        data = self.get_ads_data(relationship, lang, limit)
        if lang is None:
            lang = data['lang']
        rootstyle = ['margin-left: 0']  # aus (gf) templates/ad_content.pt
        if not data['number']:  # leeren Container nicht anzeigen:
            rootstyle.append('display: none')
        # wenn aktuell nichts konfiguriert, muß dennoch nach angemessener Zeit
        # neu nachgesehen werden
        kwargs = {'class': 'ads-content',     # aus (gf) templates/ad_content.pt
                  'style': ';'.join(rootstyle),
                  'data-relation': relationship,
                  'id': 'ads-'+relationship,
                  }
        root = Element('div', **kwargs)
        container = SubElement(root, 'div', **{'class': 'ads-array'})
        i = 0
        index = data['index']
        while True:
            if i >= data['number']:
                break
            i += 1
            # print i, data['number']
            adict = data['ads'][index]
            url = adict['link2url'] or None
            if url is not None:
                addto = SubElement(container, 'a',
                                   target='_blank',
                                   href=url)
            else:
                addto = container
            img = SubElement(addto, 'img',
                             src=adict['img_src'],
                             alt=ALT_TEXT[lang])
            index = next_of(data['adslength'], index)
        if not i:  # '<div/>' vermeiden!
            dummy = SubElement(container, 'span',
                               style='display:none')
            dummy.text = ' '  # 'PREVENT DIV SHORTCUT'

        script = SubElement(root, 'script', type='text/javascript')
        script.text = '''
                $(document).ready(function () {
                    UnitraccAds.register(%s);
                })''' % json_dumps(data)
        return etree_tostring(root, 'utf-8')

    @ram.cache(cache_key)
    def getCached(self, relationship, recurse=False):
        portal_url = getToolByName(self.context, "portal_url")
        portal = portal_url.getPortalObject()
        return [{'getLocation': object_.getLocation(),
                 'absolute_url': localurl(object_),
                 }
                for object_
                in portal.getBrowser('stage').get(relationship,
                                                  recurse=recurse)
                ]

    def has_advertising(self):
        """
        Gibt es in dieser Unitracc-Instanz Werbung?
        """
        return self.context.getBrowser('unitraccfeature').has_advertising()

# vim: ts=8 sts=4 sw=4 si et
