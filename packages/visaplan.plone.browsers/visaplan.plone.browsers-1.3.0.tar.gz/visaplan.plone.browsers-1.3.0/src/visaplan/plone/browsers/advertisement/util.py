# -*- coding: utf-8 -*-
"""
Utility-Funktionen für unitracc@@advertisement
"""


# Python compatibility:
from __future__ import absolute_import


def striphost(url):
    """
    Entferne die Hostnamens-Komponente einer URL

    >>> striphost('http://unitracc.de/test')
    '/test'
    >>> striphost('https://unitracc.de/test2')
    '/test2'

    Solche URLs können aus fehlerhaften RewriteRules entstehen:
    >>> striphost('http://unitracc.de:/test')
    '/test'

    Hier ist nichts zu retten; es könnte sich ja um eine ansonsten harmlose Dopplung handeln:
    >>> striphost('http//unitracc.de:/test')
    'http//unitracc.de:/test'

    Bei Objekt-URLs (wie von --> localurl(o) verarbeitet, da jeweils ein Objekt
    übergeben wird) kann davon ausgegangen werden, daß die Protokollvariante
    vorhanden ist
    """
    liz = url.split('://', 1)
    if not liz[1:]:
        return url
    liz = liz[1].split('/', 1)
    return '/'.join(['']+liz[1:])


def localurl(o):
    """
    Gib die "lokale" URL des übergebenen Objekts zurück;
    Funktionslogik wie in --> striphost().

    Wird knallen für das Portalobjekt; dafür wird eine Überprüfung eingespart,
    und ein Funktionsaufruf.
    """
    liz = o.absolute_url().split('://', 1)
    liz = liz[1].split('/', 1)
    return '/'.join(['']+liz[1:])


if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()
