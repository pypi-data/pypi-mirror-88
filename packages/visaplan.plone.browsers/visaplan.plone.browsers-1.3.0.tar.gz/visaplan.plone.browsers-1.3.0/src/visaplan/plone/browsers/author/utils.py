# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et
"""
utils-Modul für @@author

Autor: Tobias Herp
"""

# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.tools.coding import safe_decode

__all__ = ('joinNonemptyAttributes',
           'get_title_and_name',
           'get_formatted_name',
           'make_getter',
           )


def joinNonemptyAttributes(dic, *attributes, **kwargs):
    """
    Gib eine Zeichenkette zurück, die aus den nicht-leeren
    Attributen des übergebenen dict-Werts gebildet wird.

    dic -- das Dictionary (z.B. aus self.getBrainByUserId)
    separator -- wenn nicht None, der zur Verkettung verwendete
                 String

    unbenannte Argumente: jeweils ein String (Attributname), oder
    ein 2-Tupel aus dem Attributnamen und einer Funktion zur
    Transformation.

    >>> dic=dict(getAcademicTitle='Dr.', getFirstname='Hase', getLastname='Caesar')
    >>> attrs=('getAcademicTitle', 'getFirstname', 'getLastname')
    >>> joinNonemptyAttributes(dic, *attrs)
    'Dr. Hase Caesar'
    >>> dic['getFirstname'] = None
    >>> joinNonemptyAttributes(dic, *attrs)
    'Dr. Caesar'

    Wenn ein unbenanntes Argument ein Tupel ist, ist dessen zweites Element eine
    Transformationsfunktion:

    >>> from string import upper
    >>> attrs=('getAcademicTitle', 'getFirstname', ('getLastname', upper))
    >>> joinNonemptyAttributes(dic, *attrs)
    'Dr. CAESAR'

    Unabhängig vom Separator ist das Ergebnis immer der Leerstring (logisch
    False), wenn alle fraglichen Werte leer sind:

    >>> ' '.join([])
    ''
    """
    res = []
    separator = kwargs.pop('separator', u' ')
    assert not kwargs, 'nur "separator" erlaubt (%s)' % kwargs
    func = None
    for aname in attributes:
        if isinstance(aname, tuple):
            aname, func = aname
        try:
            aval = dic[aname]
            if not aval:
                func = None
                continue
            aval = safe_decode(aval)
            if func is None:
                res.append(aval)
            else:
                aval = func(aval)
                func = None
                if not aval:
                    continue
                res.append(aval)
        except KeyError:
            pass
    if separator is None:
        return res
    return separator.join(res)


def get_title_and_name(brain):
    """
    Gib Titel, Vor- und Nachnamen zurück

    >>> dic=dict(getAcademicTitle='Dr.', getFirstname='Hase',
    ...          getLastname='Caesar', ignored='ignorierter Wert')
    >>> get_title_and_name(dic)
    'Dr. Hase Caesar'

    Siehe auch visaplan.plone.tools.brains.make_collector
    """
    return joinNonemptyAttributes(brain,
                                  'getAcademicTitle',
                                  'getFirstname',
                                  'getLastname',
                                  )


def get_formatted_name(brain):
    """
    Gib Vor- und Nachnamen zurück

    >>> dic=dict(getAcademicTitle='Dr.', getFirstname='Hase',
    ...          getLastname='Caesar', ignored='ignorierter Wert')
    >>> get_formatted_name(dic)
    'Hase Caesar'
    """
    return joinNonemptyAttributes(brain,
                                  'getFirstname',
                                  'getLastname',
                                  )

def make_getter(brain):
    """
    Erzeuge einen "Getter", der String-Werte aus dem übergebenen dict-Objekt
    extrahiert und generell um randständigen Weißraum bereinigt.

    >>> brain = {1: '  eins  '}
    >>> get = make_getter(brain)
    >>> get(1)
    'eins'

    Fehlende Schlüssel zeitigen Leerstrings:

    >>> get(2)
    ''
    """
    get = brain.get
    def getter(key):
        try:
            return get(key, '').strip()
        except KeyError:
            return ''
    return getter

if __name__ == "__main__":
    # Standard library:
    import doctest
    doctest.testmod()
