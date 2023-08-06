# -*- coding: utf-8 -*- äöü
# Verwendet vom transform-Browser
# (transformBookLinks bzw. transform_booklinks);
# siehe auch --> @numbertag

# Python compatibility:
from __future__ import absolute_import

# 3rd party:
from bs4 import BeautifulSoup

# visaplan:
from visaplan.kitchen.spoons import extract_uid
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.context import make_brainGetter

# Logging / Debugging:
import logging

LOGGER = logging.getLogger('unitracc@@picturenumber')
ERROR = LOGGER.error
INFO = LOGGER.info

# from pprint import pprint

def counted_image(brain):
    return brain.portal_type == 'UnitraccImage'


def counted_formula(brain):
    return brain.getContentType == 'text/html'

CLS2CHECKFUNC = {
        'book-link-image': counted_image,
        'book-link-formula': counted_formula,
        }


class IPictureNumber(Interface):

    def get(haystack_uid, needle_uid, class_):
        """ """


class Browser(BrowserView):

    implements(IPictureNumber)

    def get(self, haystack_uid, needle_uid, class_):
        """
        Durchsuche den Text (getRawText) des Katalogobjekts mit der UID
        <haystack_uid> nach <img>-Elementen.  Wenn ein passendes Element gefunden
        wird, gib die Nummer desselben im Kontext des Katalogobjekts zurück.
        """
        counter = 0
        if not haystack_uid or not needle_uid:
            return counter
        context = self.context
        transform = context.getBrowser('transform')
        getbrain = make_brainGetter(context)

        found = False
        try:
            func = CLS2CHECKFUNC[class_]
        except KeyError:
            ERROR('get(%(haystack_uid)r, %(needle_uid)r, %(class_)r): '
                  'Falscher Wert für Klasse',
                  locals())
            return counter

        current = getbrain(haystack_uid)
        if current:
            soup = BeautifulSoup(str(current.getRawText))
            for elem in soup.find_all('img'):
                src = elem.attrs.get('src')
                if not src:
                    continue
                uid = extract_uid(src)
                if not uid:
                    continue
                brain = getbrain(uid)
                if not brain:
                    if uid == needle_uid:
                        ERROR('get(%(haystack_uid)r, %(needle_uid)r, %(class_)r): '
                              'getbrain(needle_uid) nicht erfolgreich',
                              locals())
                        return 0
                    elif uid == haystack_uid:
                        ERROR('get(%(haystack_uid)r, %(needle_uid)r, %(class_)r): '
                              'getbrain(haystack_uid) nicht erfolgreich',
                              locals())
                        return 0
                    else:
                        ERROR('get(%(haystack_uid)r, %(needle_uid)r, %(class_)r): '
                              'konnte UID %(uid)r nicht aufloesen',
                              locals())
                    continue
                if func(brain):
                    counter += 1
                    if uid == needle_uid:
                        found = True
                        return counter
        if not found:
            ERROR('get(%(haystack_uid)r, %(needle_uid)r, %(class_)r): '
                  'needle_uid nicht gefunden',
                  locals())
