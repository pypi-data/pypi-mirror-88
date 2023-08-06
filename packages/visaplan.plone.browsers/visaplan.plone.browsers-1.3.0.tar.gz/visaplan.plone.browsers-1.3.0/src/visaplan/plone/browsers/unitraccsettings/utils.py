# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

from six import string_types as six_string_types

# Standard library:
from binascii import hexlify
from os.path import join

# --------------------------------------------------- [ Daten ... [
LINESEPS = frozenset('\r\n')
# --------------------------------------------------- ] ... Daten ]


def make_formfields(dic):
    """
    Wandle ein dict um in eine Liste, die zur Konstruktion von Formulardaten verwendet werden kann
    (siehe http://old.zope.org/Members/Zen/howto/FormVariableTypes, http://dev-wiki.unitracc.de/wiki/Typenkonversion_in_Zope-Formularen)

    >>> make_formfields({'key': 'Wert'})
    [{'id': 'key', 'name': 'key', 'value': 'Wert'}]
    """
    res = []
    if dic is None:
        return res
    prefix = ''
    _make_formfields(dic, res, prefix)
    return res


# -------------------------------------------- [ Hilfsfunktionen ... [
def _make_formfields(dic, res, prefix, suffix=''):
    for key, val in dic.items():
        if isinstance(key, six_string_types):
            dic = {'id': key,
                   'name': prefix+key+suffix,
                   'value': val,
                   }
            _type = _typeval(key, val)
            if _type is not None:
                dic['type'] = _type
            res.append(dic)
        else:
            raise ValueError('%(key)r --> %(val)r: not supported'
                             % locals())


def _typeval(key, val):
    if isinstance(val, six_string_types):
        if LINESEPS.intersection(val):
            return 'text'
        if key.endswith('_domains'):
            return 'text'
    # return 'pformat'


def make_path_maker(base_path):
    """
    Gib eine Funktion zurück, die den vollständigen Pfad einer Pickle-Datei erzeugt;
    es werden als 2-Tupel der Verzeichnis- und der vollständige Dateiname zurückgegeben
    """
    def get_full_paths(oid, key):
        # aus ZODB.blob.BushyLayout().oid_to_path:
        directories = ['0x%s' % hexlify(byte)
                       for byte in str(oid)
                       ]
        relative_path = '/'.join(directories)
        filename = ''.join(directories)
        dirname = join(base_path, relative_path)
        fullfilename = join(dirname, filename + '.' ) + key
        return (dirname,
                fullfilename,
                )

    def no_basepath(*args, **kwargs):
        txt = ', '.join(args + [
                        '%s=%r' % tup
                        for tup in kwargs.items()
                            ])
        raise ValueError('make_path_maker(%r))(%s)' % (base_path, txt))

    if base_path:
        return get_full_paths
    else:
        return no_basepath


def vanilla_factory(data, **kwargs):
    """
    Für _getInherited: simple Rückgabe des konfigurierten Wertes;
    brain-, uid- oder distance-Argumente werden ignoriert.

    >>> vanilla_factory(data='data', distance=0)
    'data'
    """
    return data
# -------------------------------------------- ] ... Hilfsfunktionen ]
