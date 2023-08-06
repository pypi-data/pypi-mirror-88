# -*- coding: utf-8 -*- äöü
"""
Daten für den Browser @@event
"""

# Python compatibility:
from __future__ import absolute_import

NAECHSTE_10 = '10'
# beginnt immer am ersten des aktuellen Monats:
GLEITENDES_QUARTAL = '90'
MANUAL_RANGE = '-1'
HEUTE = '1'
GLEITENDE_WOCHE = '7'
GLEITENDER_MONAT = '30'
GLEITENDES_JAHR = '365'  # Default für manual_range
DEFAULT_RANGE = NAECHSTE_10

RANGE_CHOICES = [(HEUTE,              'today'),
                 (GLEITENDE_WOCHE,    'next week'),
                 (GLEITENDER_MONAT,   'next month'),
                 (GLEITENDES_QUARTAL, 'next 3 months'),
                 (NAECHSTE_10,        'next 10 events'),
                 (MANUAL_RANGE,       'manual choice'),
                 ]
RANGE_KEYS = set(dict(RANGE_CHOICES).keys())
RANGE_KEYS.update([GLEITENDES_JAHR])

PUBLIC_STATES = ['inherit', 'published']


def get_range(form):
    """
    Gib die Auswahl für den Datumsbereich zurück

    Die Auswahl wird stets als String zurückgegeben:
    >>> form = {'range': 30}
    >>> get_range(form)
    '30'

    Das Wert ist allerdings als Zahl interpretierbar:
    >>> get_range({'range': ''})
    Traceback (most recent call last):
      ...
    ValueError: invalid literal for int() with base 10: ''

    Wenn die Formulardaten keine range-Angabe enthalten,
    kommt der Vorgabewert zurück:
    >>> get_range({}) == DEFAULT_RANGE
    True
    """
    raw = form.get('range', DEFAULT_RANGE)
    int(raw)
    raws = str(raw)
    if raws in RANGE_KEYS:
        return raws
    raise ValueError('Undefined range: %(raw)r' % locals())


if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()
