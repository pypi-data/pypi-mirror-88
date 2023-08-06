# -*- coding: utf-8 -*-
'''
Created on 04.11.2013

@author: enrico

'''
# Python compatibility:
from __future__ import absolute_import

# Standard library:
from datetime import datetime

strptime = datetime.strptime
# Standard library:
import xml.etree.cElementTree as ET
from collections import defaultdict

# Zope:
from DateTime import DateTime

shortlanguage = defaultdict(lambda: 'de')
shortlanguage['deutsch'] = 'de'
shortlanguage['englisch'] = 'en'
shortlanguage['spanisch'] = 'es'
shortlanguage['french'] = 'fr'

DEBUG = 0
if DEBUG or 1:
    # Logging / Debugging:
    import pdb

# generisch behandelbare W3L-Felder,
# und die entsprechenden Unitracc-Namen:
# (noch nicht verwendet)
w3l2unitracc = {'Sprache': 'language',
                'Bezeichnung': 'title',
                'DatumStatus': 'publish',
                }

# -------------------------------------- [ Konversionsfunktionen ... [
def cvt_echo(txt):
    """
    gib den Wert unverändert zurück
    """
    try:
        return txt.strip()
    except AttributeError:
        if not txt:
            return ''
        else:
            raise

def cvt_european_date(txt):
    return strptime(txt, "%d.%m.%Y")

def cvt_european_datetime(txt):
    try:
        dt = strptime(txt, "%d.%m.%Y %H:%M")
    except ValueError:
        dt = strptime(txt, "%d.%m.%Y")
    return DateTime(dt.strftime("%Y/%m/%d %H:%M"))

def cvt_language(txt):
    if txt in list(shortlanguage.values()):
        return txt
    return shortlanguage[txt]

# Konverter-Map; Schlüssel: Unitracc-Feldnamen
u_converter = defaultdict(lambda: cvt_echo)
u_converter['publish'] = cvt_european_date
u_converter['language'] = cvt_language
u_converter['start'] = cvt_european_datetime
u_converter['end'] = cvt_european_datetime

def unitracc_convert(field, data):
    f = u_converter[field]
    return f(data)

# -------------------------------------- ] ... Konversionsfunktionen ]

class Fileprocessor(object):
    '''
    TH: noch gibt es keinerlei zwingenden Grund für diese Klasse ...

    '''

    @staticmethod
    def parseXML(fields, optionalfields, xmlfile, w3lformat=False):
        """
        fields - alle Pflichtfelder (je nach Typ)
        optionalfields - alle weiteren vorkommenden Felder
        xmlfile - der XML-Text
        w3lformat - für Import von W3L-Exporten

        Gibt ein 2-Tupel zurück:
        - Liste der ermittelten Elemente, jeweils als dict
        - Liste von Fehlermeldungen
        """
        xml = ET.parse(xmlfile)
        fp = Fileprocessor()
        default_fields = dict((f, None) for f in fields)
        default_opt = dict((f, None) for f in optionalfields)
        result = []
        # Für jedes Objekt im Dokument:
        errormsg = list()
        for elem in xml.getroot():
            attr_dict = dict(default_fields)
            complete = True
            error = False
            title = ""

            if w3lformat:
                # opt_dict = dict(default_opt)
                if DEBUG and 1:
                    pdb.set_trace()
                # W3L Format (Nicht UNITRACC KONFORM)
                for tag in elem:
                    name = tag.get('name')
                    if name == "Bezeichnung":
                        attr_dict['title'] = fp._getText(tag)
                        title = tag.text
                    elif name == "Erklaerung":
                        children = tag.getchildren()
                        if children:
                            content = [fp._getText(tag)]
                            for child in children:
                                content.append(fp._getText(child))
                                content.append(child.tail)
                            content.append(tag.tail)
                            content = " ".join([txt for txt in content
                                                if txt])
                            attr_dict['content'] = "<p>" + content + "</p>"
                            # attr_dict['description'] = content
                            continue

                        attr_dict['content'] = "<p>" + fp._getText(tag) + "</p>"
                        #Inhalt nicht duplizieren, daher auskommentiert:
                        # attr_dict['description'] = fp._getText(tag)

                    elif name == "DatumStatus":
                        attr_dict['publish'] = cvt_european_date(tag.text)
                    elif name == "Sprache":
                        attr_dict['language'] = cvt_language(tag.text)
            else:
                opt_dict = {} # hier nicht mehr benötigt
                if DEBUG and 1:
                    pdb.set_trace()
                for tag in elem:
                    # Tag in den defined Fields?
                    tagname = tag.tag
                    name = tagname.lower()
                    text = fp._getText(tag)
                    attr_dict[name] = unitracc_convert(name, text)
            # Check ob alle required fields gefüllt sind
            for key in fields:
                if not attr_dict.get(key):
                    complete = False
            if complete and not error:
                # attr_dict.update(opt_dict)
                result.append(attr_dict)
        return result, errormsg

    @staticmethod
    def _getText(element):
        # Frage TH: warum kein Leerstring?
        try:
            text = element.text or ' '
        except TypeError:
            text = " "
        try:
            return text.strip()
        except AttributeError:
            if not text:
                return ''
            else:
                raise
        return text
