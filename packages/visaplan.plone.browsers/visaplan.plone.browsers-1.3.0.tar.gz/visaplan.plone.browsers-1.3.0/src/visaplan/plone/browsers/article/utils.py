# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et tw=72
u"""\
utils-Modul zum Browser unitracc@@article

Die Verkettung der replace-Aufrufe sollte sehr performant sein,
weil das String-Objekt nur kopiert wird wenn nötig:

>>> s1 = 'a string'
>>> s2 = s1.replace('b', 'c')
>>> s1 == s2
True
>>> s1 is s2
True
"""


# Python compatibility:
from __future__ import absolute_import


def extract_1st_image_src(text, scaling):
    """
    Extrahiere die URL des ersten Bilds aus dem übergebenen HTML-Text
    und gib sie zurück.

    Achtung: Es findet (noch) kein echtes HTML-Parsing statt!
             Es wird schlicht der Inhalt des ersten src-Attributs verwendet -
             oder des ersten Attributs, dessen Name auf 'src' endet!

    >>> extract_1st_image_src('', '240x240')
    >>> txt='<img src="/bild.jpg" alt="">'
    >>> extract_1st_image_src(txt, '240x240')
    '/bild.jpg/@@scaling/get?scaling=240x240'

    Eine etwa schon angegebene Skalierung wird entfernt und übersteuert:
    >>> txt='<img src="/bild.jpg?scaling=560x560" alt="">'
    >>> extract_1st_image_src(txt, '240x240')
    '/bild.jpg?scaling=240x240'
    """
    links = text.split('src="')
    if links[1:2]:  # ... also Länge > 1, und Index 1 existiert
        link = (links[1].split('"')[0]
                .replace('/image_mini', '')
                .replace('/image_preview', '')
                .replace('/image_thumb', '')
                )
        head = link.split('/')[0]
        if head in ('resolveuid',
                    'resolveUid',
                    ):
            link = '/'+link
        if link.find('scaling') != -1:
            return link.split('?')[0] + '?scaling=' + scaling
        else:
            return link + '/@@scaling/get?scaling=' + scaling


if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()
