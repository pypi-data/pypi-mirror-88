# -*- coding: utf-8 -*- äöü
"""\
Daten-Modul für unitracc@@changestate
"""

# Python compatibility:
from __future__ import absolute_import

# Standard library:
from collections import defaultdict

# visaplan:
from visaplan.tools.minifuncs import gimme_None

initial_publication_transition = defaultdict(gimme_None)
initial_publication_transition.update({
    # standardmäßig für Alle:
    'UnitraccNews':         'make_public',
    'UnitraccArticle':      'make_public',
    'UnitraccEvent':        'make_public',
    'UnitraccFile':         'make_public',
    'UnitraccImage':        'make_public',
    'UnitraccTable':        'make_public',
    'UnitraccFormula':      'make_public',
    'UnitraccLiterature':   'make_public',
    'UnitraccBinary':       'make_public',
    'UnitraccAnimation':    'make_public',
    'UnitraccAudio':        'make_public',
    'UnitraccVideo':        'make_public',
    # standardmäßig für Angemeldete:
    'UnitraccGlossary':     'make_visible',
    'UnitraccStandard':     'make_visible',
    # standardmäßig für Teilnehmer:
    'UnitraccCourse':       'make_restricted',
    })

# ----------------------- [ Symbole, inbesondere zum Importieren ... [
INHERIT =    'inherit'
PRIVATE =    'private'
SUBMITTED =  'submitted'
ACCEPTED =   'accepted'
APPROVED =   'approved'
RESTRICTED = 'restricted'
VISIBLE =    'visible'
PUBLISHED =  'published'
# ----------------------- ] ... Symbole, inbesondere zum Importieren ]

_numeric_status_level = {
        'inherit':     None,
        'private':       10,
        'submitted':     20,
        'accepted':      30,
        'approved':      40,
        'restricted':   100,
        'visible':      110,
        'published':    120,
        }
_approval_level = _numeric_status_level['approved']
_min_publication_level = _numeric_status_level['restricted']
assert _approval_level <= _min_publication_level

_transition_target = {
        'make_restricted': 'restricted',
        'make_visible': 'visible',
        'make_public': 'published',
        }
_transition_target_numeric = {
        key: _numeric_status_level[_transition_target[key]]
        for key in _transition_target.keys()
        }
