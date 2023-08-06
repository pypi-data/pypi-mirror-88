# -*- coding: utf-8 -*- äöü
"""
unitracc@unitracctype.utils
"""

# Python compatibility:
from __future__ import absolute_import


def sorted_by_label(tuplist, translate):
    """
    tuplist -- eine Sequenz von Tupeln (Wert, Label)
    translate -- eine Funktion zur Übersetzung der Label

    Wenn die Übersetzung eines Labels (erwartungsgemäß) ungleich seiner Urform ist,
    wird die Urform in Klammern ergänzt.
    Das Ergebnis wird nach den so gebildeten Labeln sortiert.

    >>> tuples = (('val1', 'label 1'), ('val2', 'Label 3'), ('val3', 'LABEL 2'))
    >>> from string import upper
    >>> sorted_by_label(tuples, upper)
    [('val1', 'LABEL 1 (label 1)'), ('val3', 'LABEL 2'), ('val2', 'LABEL 3 (Label 3)')]
    """
    tmpl = []
    for k, v in tuplist:
        v2 = translate(v)
        if v2 != v:
            v = '%s (%s)' % (v2, v)
        tmpl.append((v, k))  # wg. Sortierung
    tmpl.sort()
    return [(tup[1], tup[0])
            for tup in tmpl
            ]


if __name__ == '__main__':
    # Standard library:
    from doctest import testmod
    testmod()
