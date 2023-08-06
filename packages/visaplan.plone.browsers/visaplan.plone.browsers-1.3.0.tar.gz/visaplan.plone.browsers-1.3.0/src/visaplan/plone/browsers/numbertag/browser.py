# -*- coding: utf-8 -*- äöü
# Python compatibility:
from __future__ import absolute_import

# Standard library:
import re

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.context import getbrain

# Logging / Debugging:
from visaplan.tools.debug import pp

# Verwendet vom transform-Browser
# (transformBookLinks bzw. transform_booklinks);
# siehe auch --> @picturenumber

# from pprint import pprint

class INumberTag(Interface):

    def get(haystack_uid, needle_uid):
        """ """


class Browser(BrowserView):

    implements(INumberTag)

    def get(self, haystack_uid, needle_uid, class_):
        """
        Durchsuche den Text (getRawText) des Katalogobjekts mit der UID
        <haystack_uid> nach <a>-Elementen.  Wenn ein passendes Element gefunden
        wird, gib die Nummer desselben im Kontext des Katalogobjekts zurück.
        """
        counter = 0
        if 0:
            pp((('haystack:', haystack_uid),
                ('needle:  ', needle_uid),
                ('class_:  ', class_),
                ))
        if not haystack_uid or not needle_uid:
            return counter
        context = self.context
        current = getbrain(context, haystack_uid)
        if current:
            text = str(current.getRawText)

            tags = [item[0] for item in re.findall(r'(\<(a)[^<]*</a>)', text)]

            orderNumberInPage = 0

            for tag in tags:
                if tag.find(class_) != -1:
                    counter += 1
                    if tag.find(needle_uid) != -1:
                        return counter

        return counter
