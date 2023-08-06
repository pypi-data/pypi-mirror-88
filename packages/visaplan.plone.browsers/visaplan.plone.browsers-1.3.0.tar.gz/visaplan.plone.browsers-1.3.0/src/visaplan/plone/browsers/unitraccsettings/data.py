# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=79
"""\
Daten für unitracc@@unitraccsettings
"""
# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.search.unitraccsearch.data import (
    localsearch_json_presets_default,
    )

# ------------------------------------------------------ [ Daten ... [
BASE = [
    {'key': 'localsearch_json_presets',
     'configpage': {'path': '/manage_localsearch_json_preset',
                    'label': 'Display presets for local search'},
     'default': localsearch_json_presets_default,
     },
    {'key': 'config_mainpage',
     'configpage': {'path': '/configure_mainpage',
                    'label': 'Configure mainpage'},
     'default': {'folder_uid': '66241bdd39f2341bc91148e26052dffa',
                 'page_uid': 'f1bce398a8269e3b5f468373596e9a0c'}
     },
    {'key': 'industrialdropdownselection',
     'configpage': {'path': '/configure-industrial-drop-down',
                    'label': 'Konfiguration Know-How Bereich'},
     'default': {
         'relationships': 'PB@@Planning, Dimensioning\r\n'
                          'IN@@Inspection\r\n'
                          'VL@@Trenchless installation\r\n'
                          'RA@@Limiting conditions\r\n'
                          'EG@@Replacement by trenchless method\r\n'
                          'OB@@Open cut method\r\n'
                          'RN@@Renovation\r\n'
                          'RP@@Repair\r\n'
                          'RE@@Cleaning',
         'changeFrom': '',
         'changeTo': '',
         'EG@@Replacement by trenchless method': {
             'sublevel': 'EGBD@@Pipe bursting, pneumatic\r\n'
                         'EGBH@@Pipe bursting, hydraulic'},
         'IN@@Inspection': {
             'sublevel': 'INDP@@Leaktightness testing\r\n'
                         'INKB@@Classification and evaluation'},
         'OB@@Open cut method': {
             'sublevel': 'OBGV@@Trench lining\r\n'
                         'OBNO@@New construction, open cut method'},
         'PB@@Planning, Dimensioning': {
             'sublevel': 'PBST@@Structural calculations\r\n'
                         'PBLN@@Piping network\r\n'
                         'PBGR@@Soil Mechanics\r\n'
                         'PBHY@@Hydraulic'},
         'RA@@Limiting conditions': {
             'sublevel': 'RABO@@Soil\r\n'
                         'RAGW@@Groundwater'},
         'RE@@Cleaning': {
             'sublevel': 'REHD@@High pressure cleaning\r\n'
                         'REMR*@@Mechanical cleaning'},
         'RN@@Renovation': {
             'sublevel': 'RNA*@@Lining process\r\n'
                         'RNB*@@Coating'},
         'RP@@Repair': {
             'sublevel': 'RPGB@@Trenchless method\r\n'
                         'RPOB@@Open cut method'},
         'VL@@Trenchless installation': {
             'sublevel': 'VLRV@@Manned pipe jacking\r\n'
                         'VLSB@@Manholes and excavations\r\n'
                         'VLSEM*@@Microtunnelling\r\n'
                         'VLSES*@@Horizontal directional drilling'},
         },
     },
    {'key': 'localsearch',
     'configpage': {'path': 'configure_localsearch',
                    'label': 'Configure local search'},
     'default': {
         '0fb049890a9c46430d6cf881bf85cee6': {
             'getCustomSearch': ['partOf=technical_information_view']},
         '1255c69f5497ffb66ab21dfb9108ec4e': {
             'getCustomSearch': ['partOf=presentation_view']},
         '1486316104fa10cf224c813016119a07': {
             'getCustomSearch': ['partOf=technical_information_view']},
         '3a9367e13781ab17f952c69a8c2045c6': {
             'getCustomSearch': ['partOf=technical_information_view']},
         '44eb887e053bb4f6b612a03bb523b190': {
             'getCustomSearch': ['partOf=technical_information_view']},
         '547f9ebea5a843321c3fc0e47d42ca62': {
             'getCustomSearch': ['partOf=technical_information_view']},
         '54f98492b5266d1d613f06486da999a9': {
             'getCustomSearch': ['partOf=technical_information_view']},
         '65720e8fd26408feedd33967b978e822': {
             'getCustomSearch': ['partOf=technical_information_view']},
         '6a0f351c5dbabf99bcfea3b673acbd5c': {
             'getCustomSearch': ['partOf=technical_information_view']},
         '6c7879ebbc919b61c72f77a4a1d9474f': {
             'getCustomSearch': ['partOf=paper_view']},
         '72e1be3ea82c2741624883f8683a9077': {
             'getCustomSearch': ['partOf=technical_information_view']},
         '7dbcefcded46f02aa83458d8b13580be': {
             'getCustomSearch': ['partOf=instructions_view']},
         '86c045bc109c562f129be4ae034bf3cb': {
             'getCustomSearch': ['partOf=technical_information_view']},
         '9303f302674cb386293e2fa8ca46f7a3': {
             'getCustomSearch': ['partOf=documentation_view']},
         '94f9c255900052d01fbe49883da17b5f': {
             'getCustomSearch': ['portal_type=UnitraccNews']},
         'af0165d42aa47e21564007bdfc7aa3c2': {
             'getCustomSearch': ['portal_type=UnitraccArticle',
                                 'portal_type=UnitraccNews']},
         'bf1b218f08ab5117b66d4a87ccb49455': {
             'getCustomSearch': ['portal_type=UnitraccImage',
                                 'portal_type=UnitraccTable',
                                 'partOf=documentation_view',
                                 'partOf=instructions_view',
                                 'partOf=technical_information_view',
                                 'mediaType=video',
                                 'mediaFormat=x-shockwave-flash',
                                 'partOf=virtual_construction_view']},
         'c5391cc6b3e35e6a4f6e42a746e381a2': {
             'getCustomSearch': ['portal_type=UnitraccArticle']},
         'd52aae1057f166b1f41edc28a181e944': {
             'getCustomSearch': ['partOf=technical_information_view']},
         'd7c4772459cce3bdb805914330b7f957': {
             'getCustomSearch': ['partOf=technical_information_view']},
         'daf2498b343fbd95a99f648a99b01eda': {
             'getCustomSearch': ['partOf=technical_information_view']},
         'db50c9b898f40b43d3ba7c2190f9686d': {
             'getCustomSearch': ['partOf=technical_information_view']},
         'e7f3babe388b73b663c3fec239abf27e': {
             'getCustomSearch': ['partOf=virtual_construction_view']},
         'eab65358e793d891b3a39d9d5ce5d341': {
             'getCustomSearch': ['partOf=technical_information_view']},
         'ec5187dd3c008bc40db9e68b8f820924': {
             'getCustomSearch': ['partOf=technical_information_view']}},
     },
    {'key': 'registration',
     'configpage': {'path': '/configure_registration',
                    'label': 'Configure registration'},
     'default': {
            'bcc': 'info@unitracc.de',
            'mailFrom': 'info@unitracc.de',
            'portal_description_de': 'Webbasierte Informations-, Lehr-, Lern- und Arbeitsplattform f\xc3\xbcr den Kanal- und Rohrleitungsbau',
            'portal_description_en': 'Web-based information, teaching and working platform for sewer and pipeline construction',
            'portal_description_es': 'Plataforma de aprendizaje, de informaci\xc3\xb3n y de trabajo en l\xc3\xadnea para la construcci\xc3\xb3n de alcantarillados y tuber\xc3\xadas',
            'portal_domains': 'www.unitracc.de\r\n'
                              'www.unitracc.com\r\n'
                              'www.unitracc.es',
            'portal_id': 'UNITRACC',
            'portal_title_de': 'UNITRACC - Underground Infrastructure Training and Competence Center',
            'portal_title_en': 'UNITRACC - Underground Infrastructure Training and Competence Center',
            'portal_title_es': 'UNITRACC - Underground Infrastructure Training and Competence Center',
            },
     },
    {'key': 'replace-missing-images',
     },
    {'key': 'rssfeed',
     'configpage': {'path': '/configure_rssfeed',
                    'label': 'Configure rss'},
     },
    {'key': 'stage',
     'configpage': {'path': '/configure_stage',
                    'label': 'Configure stage'},
     'default': {
         'advertisement-content': {
             'addableTypes': ['UnitraccImage'],
             'avaliableFor': ['Document', 'Folder', 'Plone Site',
                              'UnitraccArticle', 'UnitraccEvent', 'UnitraccNews'],
             'browseStartFolder': 'a1b535251b1d6233d1dd5455783aad10',
             'condition': 'object/@@advertisement/canAdd',
             'description': '',
             'title': 'Advertisement top content area'
             },
         'advertisement-right-one': {
             'addableTypes': ['UnitraccImage'],
             'avaliableFor': ['Document', 'Folder', 'Plone Site', 'UnitraccArticle', 'UnitraccEvent', 'UnitraccNews'],
             'browseStartFolder': 'a1b535251b1d6233d1dd5455783aad10',
             'condition': 'object/@@advertisement/canAdd',
             'description': '',
             'title': 'Advertisement right'
             },
         'advertisement-right-two': {
             'addableTypes': ['UnitraccImage'],
             'avaliableFor': ['Document', 'Folder', 'Plone Site', 'UnitraccArticle', 'UnitraccEvent', 'UnitraccNews'],
             'browseStartFolder': 'a1b535251b1d6233d1dd5455783aad10',
             'condition': 'object/@@advertisement/canAdd',
             'description': '',
             'title': 'Advertisement right two'
             },
         'advertisement-search-1': {
             'addableTypes': ['UnitraccImage'],
             'avaliableFor': ['Plone Site'],
             'browseStartFolder': 'a1b535251b1d6233d1dd5455783aad10',
             'condition': '',
             'description': '',
             'title': 'Advertisement after first search element'
             },
         'advertisement-search-bottom': {
             'addableTypes': ['UnitraccImage'],
             'avaliableFor': ['Plone Site'],
             'browseStartFolder': 'a1b535251b1d6233d1dd5455783aad10',
             'condition': '',
             'description': '',
             'title': 'Advertisement after bottom element'
             },
         'book-start-page': {
             'addableTypes': ['Document'],
             'avaliableFor': ['Folder'],
             'browseStartFolder': '',
             'condition': "python:object.getLayout() in object.getBrowser('book').getBookTemplates()",
             'description': '',
             'title': 'Start page'
             },
         'creators': {
             'addableTypes': ['UnitraccAuthor'],
             'avaliableFor': ['Folder',
                              'UnitraccArticle',
                              'UnitraccEvent', 'UnitraccNews'],
             'browseStartFolder': '5fe2a19cff91d9ed9595bfdc76887a78',
             'condition': '',
             'description': '',
             'title': 'Authors'
             },
         'illustration': {
             'addableTypes': ['UnitraccImage'],
             'allowBrowse': '1',
             'avaliableFor': ['Folder'],
             'browseStartFolder': 'dc1403e8e1b25edca88f5f5a45715f3a',
             'condition': "python:object.getLayout() in object.getBrowser('book').getBookTemplates()",
             'description': '',
             'title': 'Illustration'
             },
         'list-folder-right': {
             'addableTypes': ['Document'],
             'allowBrowse': '1',
             'avaliableFor': ['Folder'],
             'browseStartFolder': '',
             'condition': "python:object.getLayout() in ['listing_folder_view',"
                                                    "'aktuelles_folder_view']",
             'description': 'Choose an article. The body is displayed on the right side.',
             'title': 'Listing folder page'
             },
         'mainpage-custom-content': {
             'addableTypes': ['Document', 'UnitraccImage'],
             'allowBrowse': '1',
             'avaliableFor': ['Document'],
             'browseStartFolder': '',
             'condition': "python:object.getLayout()=='mainpage_view'",
             'description': '',
             'title': 'Mainpage - Custom content'
             },
         'mainpage-unitracc1.0-button': {
             'addableTypes': ['UnitraccImage'],
             'allowBrowse': '1',
             'avaliableFor': ['Document'],
             'browseStartFolder': '9d8d0fbf1972fbad43ffb92e3b6b7826',
             'condition': "python:object.getLayout()=='mainpage_view'",
             'description': 'Button with link to UNITRACC 1.0',
             'title': 'Mainpage - UNITRACC 1.0 Button'
             },
         'mainpage-welcome-page': {
             'addableTypes': ['Document'],
             'allowBrowse': '1',
             'avaliableFor': ['Document'],
             'browseStartFolder': '',
             'condition': "python:object.getLayout()=='mainpage_view'",
             'description': '',
             'title': 'Mainpage - Welcome page'
             },
         'presentation-comment': {
             'addableTypes': ['Document'],
             'allowBrowse': '1',
             'avaliableFor': ['Document'],
             'browseStartFolder': '',
             'condition': "python:object.getBrowser('presentation').isPresentationPage()",
             'description': '',
             'title': 'Comment'
             },
         'presentation-sound': {
             'addableTypes': ['UnitraccFile'],
             'allowBrowse': '1',
             'avaliableFor': ['Document'],
             'browseStartFolder': '',
             'condition': "python:object.getBrowser('presentation').isPresentationPage()",
             'description': '',
             'title': 'Sound'
             },
         'related-information': {
             'addableTypes': ['ATDateRangeCriterion', 'UnitraccArticle',
                              'UnitraccEvent', 'UnitraccNews',
                              'UnitraccFile', 'UnitraccImage'],
             'avaliableFor': ['UnitraccArticle',
                              'UnitraccEvent', 'UnitraccNews'],
             'browseStartFolder': '',
             'condition': '',
             'description': 'Here you can add files wich relates to the current Article',
             'title': 'Related Information'
             },
         'relationships': 'related-information\r\n'
                          'stage\r\n'
                          'list-folder-right\r\n'
                          'creators\r\n'
                          'illustration\r\n'
                          'presentation-comment\r\n'
                          'presentation-sound\r\n'
                          'mainpage-welcome-page\r\n'
                          'mainpage-custom-content\r\n'
                          'mainpage-unitracc1.0-button\r\n'
                          'unitracc-prolog\r\n'
                          'unitracc-epilog\r\n'
                          'book-start-page\r\n'
                          'unitracc-partner\r\n'
                          'advertisement-content\r\n'
                          'advertisement-right-one\r\n'
                          'advertisement-right-two\r\n'
                          'advertisement-search-1\r\n'
                          'advertisement-search-bottom',
         'stage': {
             'addableTypes': ['UnitraccImage'],
             'allowBrowse': '1',
             'avaliableFor': ['Document', 'Folder'],
             'browseStartFolder': '',
             'condition': '',
             'description': 'Add images for top banner area',
             'title': 'Banner'
             },
         'unitracc-epilog': {
             'addableTypes': ['Document'],
             'allowBrowse': '1',
             'avaliableFor': ['Folder'],
             'browseStartFolder': '',
             'condition': "python:object.getLayout() in ["
                              "'presentation_folder_view',"
                              "'glossary_folder_view',"
                              "'documentation_folder_view',"
                              "'technical_information_folder_view',"
                              "'glossary_folder_view',"
                              "'paper_folder_view',"
                              "'standard_folder_view',"
                              "'instructions_folder_view']",
             'description': '',
             'title': 'Schlusstext'
             },
         'unitracc-partner': {
             'addableTypes': ['UnitraccContact'],
             'allowBrowse': '1',
             'avaliableFor': ['Folder'],
             'browseStartFolder': '',
             'condition': "python:object.getLayout()"" in object.getBrowser('book').getBookTemplates() or object.getLayout() in object.getBrowser('presentation').getPresentationTemplates()",
             'description': '',
             'title': 'Partner'
             },
         'unitracc-prolog': {
             'addableTypes': ['Document'],
             'allowBrowse': '1',
             'avaliableFor': ['Folder'],
             'browseStartFolder': '',
             'condition': "python:object.getLayout() in ["
                              "'presentation_folder_view',"
                              "'glossary_folder_view',"
                              "'documentation_folder_view',"
                              "'technical_information_folder_view',"
                              "'glossary_folder_view',"
                              "'paper_folder_view',"
                              "'standard_folder_view',"
                              "'instructions_folder_view']",
             'description': '',
             'title': 'Einleitung'
             },
         }
     },
    {'key': 'subportal',
     'configpage': {'path': '/configure_subportal',
                    'label': 'Subportal configuration'},
     'default': {
         'default_uid': '5d6e59acb400c543e3318411be404685',
         '5d6e59acb400c543e3318411be404685': {
             'booking_bic': '',
             'booking_email': 'orders@unitracc.de',
             'booking_iban': '',
             'css': '',
             'domains': 'http://unitracc.de\r\n'
                        'http://www.unitracc.de\r\n'
                        'http://unitracc.com\r\n'
                        'http://www.unitracc.com\r\n'
                        'http://unitracc.es\r\n'
                        'http://www.unitracc.es\r\n'
                        'http://unitracc.unitracc1.vcl1.vdz.kunden.csl.de',
             'gacode': 'UA-2368935-1',
             'js': '',
             'languages': 'de;Deutsch\r\n'
                          'en;English\r\n'
                          'es;Espa\xc3\xb1ol',
             'logo': '',
             'logoright': 'de;logo_stein_und_partner.png;http://www.stein.de\r\n'
                          'en;logo_stein_und_partner.png;http://www.stein.de\r\n'
                          'es;logo_stein_und_partner.png;http://www.stein.de',
             'paypal_id': 'payment@knowledge-factory.de',
             'paypal_url': 'https://www.paypal.com/de/cgi-bin/webscr',
             'portal_title': 'UNITRACC - Underground Infrastructure Training and Competence Center',
             'team_email': 'info@unitracc.de',
             'title': 'UNITRACC',
             'vat_id': ''},
         'e440a5224bdca62aba656fb6d4b820a1': {
             'booking_bic': '',
             'booking_email': '',
             'booking_iban': '',
             'css': 'bootstrap.aqwa.css',
             'domains': 'http://aqwa.unitracc.de\r\n'
                        'http://aqwa-spare.unitracc.de\r\n'
                        'http://www.aqwa-academy.de\r\n'
                        'http://aqwa-academy.de\r\n'
                        'http://www.aqwa-academy.com\r\n'
                        'http://aqwa-academy.com\r\n'
                        'http://www.aqwa-academy.net\r\n'
                        'http://aqwa-academy.net\r\n'
                        'http://www.aqwa-academy.org\r\n'
                        'http://aqwa-academy.org\r\n'
                        'http://www.aqwa-academy.eu\r\n'
                        'http://aqwa-academy.eu\r\n'
                        'http://aqwa-plone4.unitracc.de\r\n'
                        'http://aqwa.vbox-therp.sbs-sup.local\r\n'
                        'http://aqwa.unitracc1.vcl1.vdz.kunden.csl.de',
             'gacode': 'UA-2368935-4',
             'js': 'aqwa.js',
             'languages': 'de;Deutsch\r\n'
                          'en;English',
             'logo': 'aqwa-academy.png',
             'logoright': 'de;logo_bmbf_de_small.png;http://www.bmbf.de/\r\n'
                          'en;logo_bmbf_en_small.png;http://www.bmbf.de/',
             'paypal_id': '',
             'paypal_url': 'https://www.sandbox.paypal.com/de/cgi-bin/webscr',
             'portal_title': 'AQWA Academy',
             'team_email': '',
             'title': 'AQWA Academy',
             'vat_id': ''},
         },
     },
    {'key': 'tcconvert',
     }
    ]

# --------------- [ erzeugt aus BASE (siehe init-Funktion) ... [
DEFAULT = {}  # Default-Werte; erzeugen passende Formularfelder
CONFIGPAGE = {}  # spezialisierte Konfigurationsseiten
READONLY = {}  # Wenn spez. Konf.seiten vorhanden sind, können
               # Änderungen nur in diesen vorgenommen werden;
               # Ausnahme: "Reset" auf Vorgabewerte
# --------------- ] ... erzeugt aus BASE (siehe init-Funktion) ]
# ------------------------------------------------------ ] ... Daten ]


def init():
    DEFAULT.update([(dic['key'], dic['default'])
                    for dic in BASE
                    if 'default' in dic
                    ])
    for dic in BASE:
        try:
            configpage = dic['configpage']
        except KeyError:
            pass
        else:
            path = configpage.get('path')
            label = configpage.get('label')
            # "globale" Konfigurationsseiten haben einen Pfad mit führendem
            # Schräger, "lokale" (Kontextabhängige) nicht:
            isglobal = path and path.startswith('/')
            if isglobal:
                configpage.update({
                    'isglobal': isglobal,
                    'label': label or path[1:],
                    })
            else:
                configpage.update({
                    'isglobal': isglobal,
                    'label': label or path or None,
                    })
    CONFIGPAGE.update(
                   [(dic['key'], dic['configpage'])
                    for dic in BASE
                    if 'configpage' in dic
                    ])
    READONLY.update([(dic['key'], bool(dic['configpage']['label']))
                     for dic in BASE
                     if 'configpage' in dic
                     ])


init()
