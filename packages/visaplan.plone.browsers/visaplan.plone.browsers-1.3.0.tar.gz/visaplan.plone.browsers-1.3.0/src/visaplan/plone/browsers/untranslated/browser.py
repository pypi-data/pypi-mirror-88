# -*- coding: utf-8 -*-
"""
Browser untranslated - stellt die Informationen des Moduls unitracc.typestr
für Seitentemplates zur Verfügung
"""
# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.base.typestr import plu_string, pt_string, type_string


class IUntranslated(Interface):

    def get(portal_type=None, sing=None, key=None):
        """
        Gib die (unübersetzten) Strings für den übergebenen Typ zurück.
        Es kann *entweder* der portal_type (z. B. 'UnitraccEvent') oder
        die Singularform ('event') übergeben werden;
        wird kein key übergeben, so wird das komplette dict zurückgegeben.
        """

    def fromTemplate(tid=None):
        """
        Wie get(), aber ermittle die Eingabedaten aus dem Namen des Templates.
        Zu verwenden für generische Template-Namen wie our-articles etc.

        tid -- Template-ID; wenn nicht angegeben, wird der Request verwendet.
        """


class Browser(BrowserView):

    implements(IUntranslated)

    def get(self, portal_type=None, sing=None, key=None):
        """
        Gib die (unübersetzten) Strings für den übergebenen Typ zurück.
        Es kann *entweder* der portal_type (z. B. 'UnitraccEvent') oder
        die Singularform ('event') übergeben werden;
        wird kein key übergeben, so wird das komplette dict zurückgegeben.
        """
        if portal_type is None:
            assert sing is not None, 'sing darf nicht None sein'
        else:
            assert sing is None, 'sing muß None sein'
        if key is None:
            if portal_type is None:
                return type_string[sing]
            else:
                return pt_string[portal_type]
        else:
            if portal_type is None:
                return type_string[sing][key]
            else:
                return pt_string[portal_type][key]

    def fromTemplate(self, tid=None):
        """
        Wie get(), aber ermittle die Eingabedaten aus dem Namen des Templates.
        Zu verwenden für generische Template-Namen wie our-articles etc.

        tid -- Template-ID; wenn nicht angegeben, wird der Request verwendet.
        """
        if tid is None:
            context = self.context
            request = context.REQUEST
            tmp = request.get('URL')
            tid = [p for p in tmp.split('/')
                   if p][-1]
        plu = tid.split('-')[-1]
        return plu_string[plu]
