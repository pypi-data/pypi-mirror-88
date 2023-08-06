# -*- coding: utf-8 -*- Umlaute: äöü
# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.context import getbrain, make_translator

try:
    # Zope:
    from Globals import DevelopmentMode
except ImportError:
    # Hotfix for Zope 4; how to properly replace this?
    DevelopmentMode = False

# Standard library:
from collections import defaultdict

# Local imports:
from .utils import sorted_by_label

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import log_or_trace, pp

logger, debug_active, DEBUG = getLogSupport()

lot_kwargs = {'debug_level': debug_active,
              'trace': debug_active >= 2,
              }

# ------------------------------------------------------ [ Daten ... [
# ""'...'-Strings: markiert fuer Uebersetzung
# ACHTUNG: Bitte explizit *nicht* zu uebersetzende Strings in der Liste
#          *kommentieren* - danke!
list_ = [('portal_type=UnitraccArticle',
          ""'UnitraccArticle'),
         ('portal_type=UnitraccNews',
          ""'UnitraccNews'),
         ('portal_type=UnitraccImage',
          ""'UnitraccImage'),
         ('portal_type=UnitraccStandard',
          ""'UnitraccStandard'),
         ('portal_type=UnitraccGlossary',
          ""'UnitraccGlossary'),
         ('portal_type=UnitraccTable',
          ""'UnitraccTable'),
         ('partOf=documentation_view',
          ""'Part of documentation'),
         ('layout=documentation_view',
          ""'Documentation'),
         ('partOf=instructions_view',
          ""'Part of instruction'),
         ('layout=instructions_view',
          ""'Instruction'),
         ('partOf=presentation_view',
          ""'Part of presentation'),
         ('layout=presentation_view',
          ""'Presentation'),
         ('partOf=technical_information_view',
          ""'Part of technical book'),
         ('layout=technical_information_view',
          ""'Technical book'),
         ('partOf=paper_view',
          ""'Part of paper'),
         ('layout=paper_view',
          ""'UnitraccPaper'),
         ('partOf=virtual_construction_view',
          'Part of virtual construction'),
         ('layout=virtual_construction_view',
          'Virtual construction'),
         ('portal_type=UnitraccEvent',
          ""'UnitraccEvent'),
         ('portal_type=UnitraccVideo',
          ""'Video'),
         ('portal_type=UnitraccBinary',
          ""'UnitraccBinary'),
         ('portal_type=UnitraccAnimation',
          ""'UnitraccAnimation'),
         ('portal_type=FolderishAnimation',
          ""'FolderishAnimation'),
         ('portal_type=Document',
          ""'Document'),
         ('portal_type=UnitraccAudio',
          ""'UnitraccAudio'),
         ('portal_type=UnitraccVideo',
          ""'UnitraccVideo'),
         # ('mediaFormat=x-shockwave-flash-sound',
         # 'Sound'),
         ('portal_type=UnitraccFormula',
          ""'UnitraccFormula'),
         ('portal_type=UnitraccLiterature',
          ""'UnitraccLiterature'),
         # ('portal_type=UnitraccAuthor',
         # 'UnitraccAuthor')
         # ('portal_type=UnitraccContact',
         # 'UnitraccContact')
         # benötigt für Lokale Suche:
         ('portal_type=Folder',
          ""'Folder'),
         ('portal_type=UnitraccCourse',
          ""'UnitraccCourse'),
        ]

dict_ = {}
for k, v in list_:
    dict_[k] = v

list_sorted = sorted(list_)

list2 = []
listsbycat = {}
listsbycat['image'] = []
for tup in [  # ... getTypesWithImage:
        ('portal_type=UnitraccImage',
         ""'UnitraccImage'),
        ('portal_type=UnitraccVideo',
         ""'Video'),
        ('portal_type=UnitraccFormula',
         ""'UnitraccFormula'),
        ('portal_type=UnitraccAnimation',
         ""'UnitraccAnimation'),
        ('portal_type=FolderishAnimation',
         ""'FolderishAnimation'),
        ('portal_type=UnitraccAudio',
         ""'UnitraccAudio'),
        ]:
    listsbycat['image'].append(tup)
list2.extend(listsbycat['image'])

listsbycat['non-image'] = []
imagetups = listsbycat['image']
for tup in list_:
    if tup not in imagetups:
        listsbycat['non-image'].append(tup)

list2.extend(listsbycat['non-image'])

group_headers = {'portal_type': 'by object type',
                 # 'mediaType': 'by media type',
                 'partOf': 'by type of containing structure',
                 'layout': 'by structure type',
                 'other': 'other',
                 }
list1_asdict = defaultdict(list)
for tup in list_:
    assignment, label = tup
    try:
        key, val = assignment.split('=', 1)
    except Exception:
        key = 'other'
    list1_asdict[key].append(tup)

list_of_portal_types = list1_asdict['portal_type']
if debug_active:
    pp(list_of_portal_types)

list1_grouped = []
for key in ('layout',
            'partOf',
            'portal_type',
            # 'mediaType',
            ):
    assert key in group_headers
    list1_grouped.append({'label': key,
                          'items': list1_asdict.pop(key),
                          })
for key in sorted(list1_asdict.keys()):
    if key != 'other':
        list1_grouped.append({'label': key,
                              'items': list1_asdict.pop(key),
                              })
key = 'other'
if list1_asdict[key]:
    list1_grouped.append({'label': key,
                          'items': list1_asdict.pop(key),
                          })
if debug_active:
    pp(list1_grouped=list1_grouped)


# import pdb; pdb.set_trace()
del imagetups
# ------------------------------------------------------ ] ... Daten ]


class IUnitraccType(Interface):

    def getTitle(key):
        """ """

    def get(pretty=False, grouped=False):
        """ """

    def getTypesWithImage():
        """Inhaltstypen, die Bilder enthalten, die im Inhalt verlinkt werden koennen sollen"""

    def getTypesForSearch():
        """
        Für die Erweiterte Suche (Aktivierbare Buttons)

        Alte Beschreibung:
        Typen für die Anonyme Suche (die allen zur Verfuegung steht)
        """

    def getAllSearchableTypes():
        """Suche im FCKeditor"""

    def getTypesSeekedInAllLanguages():
        """
        Typen, die von fck-search.pt stets in *allen* Sprachen gesucht werden
        """

    def getPortalTypes(pretty=True):
        """
        Gib die portal_type-Auswahl zurück
        """


class Browser(BrowserView):

    implements(IUnitraccType)

    def getTitle(self, brain):
        context = self.context
        partOf = brain.getPartOf
        title = ''
        mediaType, mediaFormat = brain.getContentType.split('/')
        if partOf:
            if 'partOf=' + brain.getLayout in dict_:
                title = dict_.get('partOf=' + brain.getLayout, '')
            else:
                title = dict_.get('partOf=' + getbrain(partOf).getLayout, '')

        if 'portal_type=' + brain.portal_type in dict_:
            title = dict_.get('portal_type=' + brain.portal_type, '')

        if 'mediaFormat=' + mediaFormat in dict_:
            title = dict_.get('mediaFormat=' + mediaFormat, '')

        if 'mediaType=' + mediaType in dict_:
            title = dict_.get('mediaType=' + mediaType, '')

        return title

    @log_or_trace(**lot_kwargs)
    def get(self, pretty=None, grouped=False):
        """
        Wenn "pretty", wird die Liste mit Hilfe des translate-Browsers übersetzt
        und nach den sichtbaren Zeichenketten sortiert; Vorgabe (vorerst): False

        Z.B. verwendet zur Konfiguration der Lokalen Suche (configure_localsearch)
        TODO: Caching des Ergebnisses (nach bool(pretty) und ggf. aktiver Sprache, nicht nach Kontext)
        """
        global list_
        if grouped:
            if pretty is None:
                pretty = True
            elif not pretty:
                logger.error('get: grouped=%(grouped)r ignoriert', locals())
        if not pretty:
            return list_
        DEBUG('get: sortiere')
        tmpl = []   # temp. list
        mogrify = make_translator(self.context)  # ggf. auch den Import wieder löschen
        if grouped:
            res = []
            for dic in list1_grouped:
                label = dic['label']
                res.append({'label': mogrify(group_headers[label]),
                            'items': sorted_by_label(dic['items'], mogrify),
                            })
            return res
        else:
            return sorted_by_label(list_, mogrify)

    def getTypesWithImage(self):
        """ """
        return [('portal_type=UnitraccImage',
                 ""'UnitraccImage'),
                ('portal_type=UnitraccVideo',
                 ""'Video'),
                ('portal_type=UnitraccFormula',
                 ""'UnitraccFormula'),
                ('portal_type=UnitraccAnimation',
                 ""'UnitraccAnimation'),
                ('portal_type=FolderishAnimation',
                 ""'FolderishAnimation'),
                ('portal_type=UnitraccAudio',
                 ""'UnitraccAudio'),
               ]

    def getTypesForSearch(self):
        """
        Für die Erweiterte Suche (Aktivierbare Buttons)

        TODO: Verwendung von list_

        Nota bene:
        - hier werden Pluralformen ausgegeben, im Unterschied zu den anderen Listen
        - Animationen und Videos werden nun nicht mehr nach mediaType/mediaFormat gesucht,
          sondern ganz normal nach portal_type.
        """
        return [('portal_type=UnitraccImage',
                 ""'Images'),
                ('portal_type=UnitraccAnimation',
                 ""'Animations'),
                ('portal_type=FolderishAnimation',
                 ""'FolderishAnimations'),
                ('portal_type=UnitraccVideo',
                 ""'Videos'),
                ('portal_type=UnitraccNews',
                 ""'News'),
                ('portal_type=UnitraccArticle',
                 ""'Articles'),
                ('partOf=technical_information_view',
                 'Technical books'),  # <--> Technical information
                ('partOf=presentation_view',
                 'Lessons'),
                ('partOf=documentation_view',
                 ""'Documentations'),
                ('partOf=instructions_view',
                 ""'Instructions'),
                ('portal_type=UnitraccGlossary',
                 ""'UnitraccGlossary_plural'),
                ('portal_type=UnitraccTable',
                 ""'UnitraccTable_plural'),
                # ('portal_type=UnitraccBinary',
                #  ""'UnitraccBinary_plural'),
                ]

    def getAllSearchableTypes(self):
        """
        Für die Suche im FCKeditor

        Liefert das Ergebnis von @@unitraccsearch.getCustomSearch();
        aufgerufen von @@unitraccsearch.search, wenn Typen weder in Formular
        angegeben noch lokal konfiguriert

        TODO: Verwendung von list_
        """
        return [('portal_type=UnitraccNews',
                 ""'UnitraccNews'),
                ('portal_type=UnitraccArticle',
                 ""'UnitraccArticle'),
                ('partOf=documentation_view',
                 ""'Documentation'),
                ('partOf=instructions_view',
                 ""'Instruction'),
                ('partOf=technical_information_view',
                 'Technical information'),  # <--> Technical books
                ('portal_type=UnitraccImage',
                 ""'UnitraccImage'),
                ('partOf=virtual_construction_view',
                 'Virtual construction'),
                ('portal_type=UnitraccVideo',
                 ""'Video'),
                ('portal_type=UnitraccTable',
                 ""'UnitraccTable'),
                ('portal_type=UnitraccBinary',
                 ""'UnitraccBinary'),
                ('portal_type=UnitraccAnimation',
                 ""'UnitraccAnimation'),
                ('portal_type=UnitraccAudio',
                 ""'UnitraccAudio'),
                ('portal_type=UnitraccVideo',
                 ""'UnitraccVideo'),
                ('portal_type=UnitraccGlossary',
                 ""'UnitraccGlossary'),
                ('portal_type=Document',
                 ""'Document'),
                ]

    def getTypesSeekedInAllLanguages(self):
        """
        Typen, die von fck-search.pt stets in *allen* Sprachen gesucht werden
        """
        return ('UnitraccFormula',
                'UnitraccLiterature',
                'UnitraccAnimation',
                # aus Konsistenzgründen, noch ohne Prüfung der Sinnhaftigkeit:
                'FolderishAnimation',
                )

    def getPortalTypes(self, pretty=True, typeonly=False):
        """
        Gib die portal_type-Auswahl zurück

        pretty -- mit übersetztem Label
        typeonly -- ohne 'portal_type='-Präfixe
        """
        types_vocab = list_of_portal_types
        if not pretty:
            return types_vocab
        DEBUG('get: sortiere')
        mogrify = make_translator(self.context)  # ggf. auch den Import wieder löschen
        if typeonly:
            return sorted_by_label([(tup[1], tup[1])
                                    for tup in types_vocab
                                    ], mogrify)
        return sorted_by_label(types_vocab, mogrify)
