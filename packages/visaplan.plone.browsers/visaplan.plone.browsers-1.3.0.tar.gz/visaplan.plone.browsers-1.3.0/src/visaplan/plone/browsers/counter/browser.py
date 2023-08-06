# -*- coding: utf-8 -*- äöü
"""
Browser unitracc@@counter: Zähler für Templates erzeugen

Der erzeugte Zähler ist eine einfache Funktion, die mit einem einfachen
Argument aufgerufen wird (dem Zähler-Schlüssel, z. B. der Template-ID);
der entsprechende Zähler wird inkrementiert und protokolliert.

Verwendungsbeispiel:

    - in html_main.pt:
      tal:define="counter nocall:context/@@counter;
                  count python:counter.get('PDF');
                  dummy python:count(templateId);
                  "

    - in weiteren Templates:
      tal:define="...;
                  dummy python:count(templateId);
                  "
"""

# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements

# Local imports:
from .utils import make_counter


class ICounterBrowser(Interface):
    """
    Interface zur Erzeugung von Zählern
    """

    def get(**kwargs):
        """
        Gib eine counter-Funktion zurück
        """

class Browser(BrowserView):

    implements(ICounterBrowser)

    def get(self, **kwargs):
        if not kwargs:
            kwargs = {'prefix': 'COUNTER'}
        return make_counter(**kwargs)


# vim: ts=8 sts=4 sw=4 si et
