# -*- coding: utf-8 -*- äöü
"""
utils-Modul für Browser nora - "news or articles"
"""

# Python compatibility:
from __future__ import absolute_import


def balanced_list(biglist, insertions,
                  idfunc=None,
                  limit=12, minimum=3,
                  start=None, step=None,
                  shortcut=True):
    """
    Erzeuge eine balancierte Liste, die mindestens <minimum>
    Elemente aus der Ergänzungsliste <insertions> enthält

    biglist - die ursprüngliche Liste, die schon Elemente der
              Ergänzungsliste enthalten kann
    insertions - die Ergänzungsliste, deren Elemente der Kategorie <cat>
                 angehören und in <biglist>
                 wahrscheinlich unterrepräsentiert sind

    Beide Listen enthalten Suchergebnisse (Singleton-Objekte, nach
    demselben Kriterium sortiert); sie sind üblicherweise kurz,
    insbesondere aber die zweite.

    idfunc - eine Funktion, die eine eindeutige ID eines Elements ermittelt

    Die Elemente der Ergänzungsliste sind - nach Maßgabe der Funktion
    <idfunc> - üblicherweise in der Ursprungsliste enthalten.

    limit - die maximale Länge der zurückzugebenden Liste.
    minimum - die anzustrebende Mindestanzahl der Elemente der Ergänzungsliste
    start - die späteste Position, an der das erste Element aus <insertions>
            in der Ergebnisliste eingefügt wird
    step - das Wiederholungsintervall für Elemente der Ergebnisliste:
           Beginnend mit <strt> ist jedes <step>. Element eines der
           Ergänzungsliste

    <start> und <step> werden, wenn nicht angegeben, aus <limit> und <minimum>
    berechnet.  Wenn sie jedoch angegeben werden, können sie auch mehr
    als <minimum> Ergänzungseelemente bewirken.

    shortcut - Wahrheitswert; Vorgabe ist True:
               Wenn die Eingangsliste kürzer als <limit> ist, wird davon
               ausgegangen, daß auch die Ergänzungsliste keine weiteren
               Elemente enthält

    >>> vowels = list('AEIOU')
    >>> consonants = list('bcdfghjklmnpqrstvwxyz')
    >>> sr1 = consonants[:12]
    >>> sr2 = vowels[:3]
    >>> kwargs = {'idfunc': lambda x: x,
    ...           'limit': 12,
    ...           'minimum': 3,
    ...           'start': 3,
    ...           'step': 3,
    ...           }

    Im realen Einsatz werden die Eingabelisten für nichts anderes
    verwendet als zur Erzeugung der ergänzten Liste; daher werden sie
    ggf. im Original geändert.

    Da dieses Verhalten die Testbarkeit beeinträchtigt, wird hier eine
    lokale Testfunktion verwendet, die Kopien der Listenargumente übergibt:

    >>> def test_balanced_list(list1, list2, *args, **kwargs):
    ...     return ''.join(balanced_list(list(list1), list(list2),
    ...                                  *args, **kwargs))
    >>> test_balanced_list(sr1, sr2[:2], **kwargs)
    'bcdAfgEhjklm'
    >>> test_balanced_list(sr1, sr2, **kwargs)
    'bcdAfgEhjIkl'

    Wenn die Ergänzungsliste zu wenige Elemente enthält oder gar leer
    ist, ist das nicht zu ändern:

    >>> test_balanced_list(sr1, sr2[:2], **kwargs)
    'bcdAfgEhjklm'
    >>> test_balanced_list(sr1, [], **kwargs)
    'bcdfghjklmnp'

    Es ist erlaubt, das erste Ergänzungselement an die erste Position zu
    stellen. In diesem Fall werden ggf. mehr als <minimum>
    Ergänzungselemente eingefügt:

    >>> kwargs['start'] = 0
    >>> test_balanced_list(sr1, vowels, **kwargs)
    'AbcEdfIghOjk'

    Wenn die Eingabeliste schon genug Elemente der Ergänzungsliste
    enthält, wird sie unverändert zurückgegeben:

    >>> sr1 = consonants[:9] + vowels[:3]
    >>> ''.join(sr1)
    'bcdfghjklAEI'
    >>> test_balanced_list(sr1, sr2, **kwargs)
    'bcdfghjklAEI'
    """
    assert limit > minimum > 0
    pool = set([idfunc(a)
                for a in insertions[:limit]
                ])
    del a
    if not pool:
        return biglist

    i = 0
    hits = 0
    hitlist = []
    for elem in biglist[:limit]:
        i += 1
        if idfunc(elem) in pool:
            hits += 1
            if hits >= minimum:
                return biglist[:limit]
            hitlist.append(i)
    # Wenn die Eingabeliste zu kurz ist, auch in der Ergänzungsliste
    # nichts erwarten:
    if i < limit and shortcut:
        return biglist

    # Vorgabewerte für step und start: noch nicht fehlerfrei ...
    if step is None:
        step, rest = divmod(limit, minimum)
        if start is None:
            start = step - 1
        if (step <= 1
            # or (rest and step < limit -1)
            ):
            step += 1
    if start is None:
        start = step - 1

    # Modifizierte Liste bauen:
    # Elemente der Ergänzungsliste zunächst entfernen ...
    hitlist.reverse()
    for i in hitlist:
        del biglist[i]
    res = list(biglist[:start])
    i = start
    chunk = step - 1
    L = start
    # ... und hier an den start-/step-Positionen einfügen:
    while L < limit:
        try:
            res.append(insertions.pop(0))
        except IndexError:
            chunk = limit
        else:
            L += 1
        res.extend(biglist[i:i+chunk])
        i += chunk
        L += chunk
    return res[:limit]


if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()
