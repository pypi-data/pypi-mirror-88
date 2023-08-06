# -*- coding: utf-8 -*- äöü
"""
utils-Modul für unitracc@@counter
"""

# Python compatibility:
from __future__ import absolute_import

# Standard library:
import random
from collections import defaultdict

# visaplan:
from visaplan.plone.tools.mock import MockLogger

# Logging / Debugging:
import logging

# ---------------------------------- [ Daten ... [
RAND_MIN = 1000
RAND_MAX = 9999
# ---------------------------------- [ Daten ... [

def make_counter(prefix, topic='template',
                 seed=None,
                 randmin=RAND_MIN, randmax=RAND_MAX):
    """
    Erzeuge ein Counter-Objekt, das z. B. bei rekursiver
    Templateverarbeitung weitergereicht werden kann.

    >>> count = make_counter('test', seed=42)
    >>> count('template_a')
    ('INFO', 'template_a -> 1')
    >>> count('template_a')
    ('INFO', 'template_a -> 2')
    >>> count('template_b')
    ('INFO', 'template_b -> 1')
    >>> count('template_a')
    ('INFO', 'template_a -> 3')
    """
    testmode = seed is not None
    if testmode:
        random.seed(seed)

    randnum = random.randint(randmin, randmax)
    pref = ('%(prefix)s [%(randnum)d] %(topic)s: ' % locals()).lstrip()
    cnt = defaultdict(int)

    if testmode:
        logger = MockLogger()
    else:
        logger = logging.getLogger(pref)

    mask1 = '%(num)4d. %(key)s'
    mask2 = mask1 + ' (%(extra)s)'

    def f1(key, extra=None):
        cnt[key] += 1
        num = cnt[key]
        logger.info(extra is None
                    and mask1
                     or mask2, locals())

    def f2(key, extra=None):
        f1(key, extra)
        return logger[-1]

    if testmode:
        return f2
    else:
        return f1


if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()
