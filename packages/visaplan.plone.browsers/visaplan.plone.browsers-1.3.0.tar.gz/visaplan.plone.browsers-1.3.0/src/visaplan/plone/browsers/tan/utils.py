# -*- coding: utf-8 -*- äöü
"""
utils-Modul des Browsers unitracc@@tan
"""

# Python compatibility:
from __future__ import absolute_import, print_function

import six
from six.moves import range

# Standard library:
from datetime import date, timedelta
from time import localtime, mktime, strftime

# Zope:
from DateTime import DateTime

# visaplan:
from visaplan.plone.tools.context import make_translator
from visaplan.tools.dates import make_date_parser

STEM_LENGTH = 7
PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)[:STEM_LENGTH]
REVERSE_PRIMES = tuple(reversed(PRIMES))
MIN_STEM = 10 ** (STEM_LENGTH - 1)
MAX_STEM = MIN_STEM * 10 - 1

TAN_LENGTH = STEM_LENGTH + 2
MIN_TAN = 10 ** (TAN_LENGTH - 1)
MAX_TAN = MIN_TAN * 10 - 1

TAN_EXAMPLE = '12.345'  # siehe unten
TAN_HELP = '%(TAN_LENGTH)d-digit number expected, e.g. %(TAN_EXAMPLE)s'

DATE_FORMAT = '%d.%m.%Y'
parse_date = make_date_parser(fmt=DATE_FORMAT)
# ACHTUNG: Änderung möglich per Monkey-Patch, z.B. im zkb-Produkt:
DEFAULT_DURATION = 31

def default_duration():
    return DEFAULT_DURATION or 31


# Testbarkeit erhalten:
DOCTEST_ONLY = __name__ == '__main__'
"""
def default_expiration_date(mask='', today=None): NUR ZUM SUCHEN!
    Wird durch Factory-Funktion erzeugt (und kann per Monkey-Patch
    durch eine in gleicher Weise erzeugte Funktion ersetzt werden):
"""
try:
    # visaplan:
    from visaplan.tools.times import make_defaulttime_calculator
except (ImportError, ValueError):
    if not DOCTEST_ONLY:
        raise
else:
    default_expiration_date = make_defaulttime_calculator(
            year=1,
            nextmonth=True,
            default_date_format=DATE_FORMAT)


def check_stem_size(stem):
    """
    Hilfsfunktion für make_tan bzw. get_check_digits:
    überprüfe die Größe der "Rumpf-TAN" (ohne Prüfziffern)

    Im Erfolgsfall passiert nichts:
    >>> check_stem_size(1234567)

    Andernfalls wird ein ValueError ausgelöst:

    >>> check_stem_size(123456)
    Traceback (most recent call last):
    ...
    ValueError: expected a value between 1000000 and 9999999; got 123456
    """
    if not MIN_STEM <= stem <= MAX_STEM:
        raise ValueError('expected a value between %d and %d;'
                         ' got %r'
                         % (MIN_STEM, MAX_STEM, stem))

def check_tan_size(tan):
    """
    Hilfsfunktion für check_tan bzw. is_valid_tan:
    überprüfe die Größe (incl. Prüfziffern).

    Im Erfolgsfall passiert nichts:
    >>> check_tan_size(123456789)

    Andernfalls wird ein ValueError ausgelöst:

    >>> check_tan_size(12345678)   # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError: ...
    """
    if not MIN_TAN <= tan <= MAX_TAN:
        raise ValueError('expected a value between %d and %d;'
                         ' got %r'
                         % (MIN_TAN, MAX_TAN, tan))

def get_check_digits(stem):
    """
    Gib die Prüfziffern für die übergebene 7-stellige "Rumpf-TAN" zurück:
    Alle Ziffern werden mit den ersten 7 Primzahlen multipliziert;
    die 100er- und höheren Stellen des Ergebnisses werden verworfen und
    die Differenz zu 99 zurückgegeben.

    >>> get_check_digits(1234567)
    96
    >>> get_check_digits(1234576)
    0
    >>> get_check_digits(1234467)
    7
    """
    val = int(stem)
    check_stem_size(val)
    sum = 0
    for fact in REVERSE_PRIMES:
        val, digit = divmod(val, 10)
        sum += digit * fact
    return 99 - (sum % 100)


def is_valid_tan(tan):
    """
    Gib einen Wahrheitswert zurück.

    Prüft die TAN lediglich auf gültige Prüfziffern
    (und nicht, ob sie verfügbar ... ist).

    tan -- die TAN als Zahl oder String

    >>> is_valid_tan('123.456.796')
    True
    >>> is_valid_tan('123.456.797')
    False
    >>> is_valid_tan(1234567)
    False
    >>> is_valid_tan(123456796)
    True

    Völlig abseitige Werte werden ebenfalls korrekt verarbeitet:

    >>> is_valid_tan('honk')
    False
    """
    try:
        check_tan(tan)
        return True
    except ValueError:
        return False

def check_tan(tan, nonempty=None, complete=False,
              translate=None, calling_self=None):
    """
    Prüfe die übergebene TAN. Wenn ok, gib den Stem zurück
    (bzw. mit complete=True die komplette TAN als Ganzzahl);
    ansonsten wirf einen ValueError.

    >>> check_tan(1.234)
    Traceback (most recent call last):
      ...
    ValueError: 9-digit number expected, e.g. 123.456.789

    >>> check_tan('123.456.796')
    1234567
    >>> check_tan('123.456.796', complete=True)
    123456796

    Wenn eine Übersetzungsfunktion "translate" oder zumindest calling_self
    übergeben wird, wird eine etwaige Fehlermeldung übersetzt; hierfür
    existieren (noch?) keine Doctests.

    Weitere Doctests: siehe is_valid_tan()
    """
    txt = None
    try:
        if not isinstance(tan, int):
            tan = tan2int(tan, nonempty)
        check_tan_size(tan)
    except ValueError:
        txt = TAN_HELP
        namespace = globals()
    if txt is None:
        stem, digits = divmod(tan, 100)
        if digits != get_check_digits(stem):
            txt = ""'check digits mismatch for tan %(tan)r'
            namespace = locals()
    if txt is not None:
        if translate is None:
            if calling_self is not None:
                translate = make_translator(calling_self.context)
        if translate is not None:
            txt = translate(txt)
        raise ValueError(txt % namespace)
    if complete:
        return tan
    return stem

INVALID_TAN_MSG = ''"The TAN %(tan)s is not valid; please check your input."
def invalid_tan_txt(tan, translate=None):
    """
    Gib eine Nachricht zurück, daß die übergebene TAN ungültig sei.
    Der Anwender wird dabei nicht darüber informiert, ob sie das
    Checksummenkriterium nicht erfüllt oder schlicht nicht vorhanden ist.
    """
    try:
        if translate:
            return translate(INVALID_TAN_MSG) % locals()
        return INVALID_TAN_MSG % locals()
    except ValueError as e:
        print(INVALID_TAN_MSG)
        print(translate)
        print(translate(INVALID_TAN_MSG))
        print(e)
        raise


def tan2int(tan, nonempty=False):
    """
    Konvertiere eine als String angegebene TAN in eine Zahl

    >>> tan2int('123.456-789')
    123456789
    >>> tan2int(' 12 34-56.78 9 ')
    123456789
    >>> tan2int('')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    ValueError: invalid literal for int() with base 10: ''

    Fehlende TANs können speziell behandelt werden:
    >>> tan2int(None, nonempty=True)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    ValueError: No TAN given!

    >>> tan2int(None)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    ValueError: Not a valid TAN: None

    Bruchzahlen sind nicht erlaubt:
    >>> tan2int(1.234)
    Traceback (most recent call last):
      ...
    ValueError: Not a valid TAN: 1.234
    """
    if tan is None and nonempty:
        raise ValueError('No TAN given!')
    try:
        val = ''.join(tan.replace('.', '').replace('-', '').split())
    except (TypeError, AttributeError):
        raise ValueError('Not a valid TAN: %(tan)r'
                         % locals())
    if nonempty and not tan:
        raise ValueError('No TAN given!')
    try:
        return int(val)
    except ValueError:
        raise ValueError('Not a valid TAN: %(val)r'
                         % locals())


def group3(tan, ch='.'):
    """
    Formatierungsfunktion für TANs

    >>> group3('1234-56789')
    '123.456.789'

    Verhalten dieser Funktion bei anderen TAN-Größen:
    >>> group3('1-2-3-4')
    '001.234'
    """
    if isinstance(tan, six.string_types):
        tan = tan2int(tan)
    res = []
    while tan:
        tan, chunk = divmod(tan, 1000)
        res.append(chunk)
    res.reverse()
    return ch.join(['%03d' % i
                    for i in res])


def tan_example(i):
    """
    >>> tan_example(7)
    1234567
    """
    assert isinstance(i, int), 'Ganze Zahl erwartet (%r)' % (i,)
    assert 1 < i < 30
    res = 0
    for j in range(1, i+1):
        res = (10 * res) + (j % 10)
    return res

TAN_EXAMPLE = group3(tan_example(TAN_LENGTH))


def make_tan(stem):
    """
    ergänze die angegebene 7-stellige TAN durch die Prüfziffern

    >>> make_tan(1234567)
    123456796
    """
    check_stem_size(stem)
    return 100 * stem + get_check_digits(stem)


def start_and_ends(form, duration, today=None):
    """
    Lies das Startdatum aus den Formulardaten (default: heute) und
    ergänze, wenn <duration> eine Zahl > 0 ist, ein entsprechendes
    Ablaufdatum.
    Es wird eine Laufzeit von <duration> vollen Tagen sichergestellt;
    bei Start <today> gibt es den angebrochenen Tag oben drauf.

    form -- die Formulardaten, ein Dictionary
    duration -- eine nichtnegative ganze Zahl, oder None
    today -- für Testbarkeit

    >>> form={'start': '2099-05-01'}
    >>> import datetime
    >>> start_and_ends(form, 10)
    {'start': datetime.date(2099, 5, 1), 'ends': datetime.date(2099, 5, 11)}
    >>> start_and_ends(form, 0)
    {'start': datetime.date(2099, 5, 1)}

    Die Schlüsselnamen 'start' und 'ends' entsprechen den Feldnamen
    in der Tabelle unitracc_groupmemberships.
    """
    return start_and_ends2(form.get('start', '').strip(),
                           duration, today)


def start_and_ends2(start=None, duration=None, today=None):
    """
    Wie start_and_ends, aber mit direkter Angabe aller beteiligten Werte
    (ohne Formular)

    start -- das Startdatum, 'YYYY-MM-DD'
    duration -- eine nichtnegative ganze Zahl, oder None
    today -- für Testbarkeit

    >>> start = '2099-05-01'
    >>> import datetime
    >>> start_and_ends2(start, 10)
    {'start': datetime.date(2099, 5, 1), 'ends': datetime.date(2099, 5, 11)}
    >>> start_and_ends2(start)
    {'start': datetime.date(2099, 5, 1)}
    >>> start_and_ends2(start, 0)
    {'start': datetime.date(2099, 5, 1)}

    Wenn nichts angegeben, kommt "heute" zurück:

    >>> heute = date(2015, 11, 5)
    >>> heute
    datetime.date(2015, 11, 5)
    >>> start_and_ends2(today=heute)
    {'start': datetime.date(2015, 11, 5)}

    Neben dem ISO-Format YYYY-mm-dd wird auch dd.mm.YYYY akzeptiert:

    >>> start = '2.5.2016'
    >>> start_and_ends2(start, 10)
    {'start': datetime.date(2016, 5, 2), 'ends': datetime.date(2016, 5, 12)}

    Die Schlüsselnamen 'start' und 'ends' entsprechen den Feldnamen
    in der Tabelle unitracc_groupmemberships.
    """
    if today is None:
        today = date.today()
    res = {}
    if start: # and not isinstance(start, datetime.date):
        start = parse_date(start)  # wirft ggf. ValueError
    if start:
        if start < today:
            raise ValueError("Please don't specify dates in the past!"
                             ' (%(start)s)'
                             % locals())
    else:
        start = today
    res = {'start': start}
    if duration:
        assert duration > 0
        if start <= today:
            duration += 1
        res['ends'] = start + timedelta(duration)
    return res


def today_matches_spec(data, today):
    """
    Liegt <today> im spezifizierten Zeitraum?

    data - ein dict mit datetime.date-Objekten für 'start'
           und (optional) 'ends'
    today - das fragliche Datum

    >>> today=date(2014, 2, 19)
    >>> spec=start_and_ends({'start': '2014-02-19'}, 0, today)
    >>> today_matches_spec(spec, today)
    True
    >>> spec=start_and_ends({'start': '2014-02-20'}, 0, today)
    >>> today_matches_spec(spec, today)
    False
    """
    if 'ends' in data and data['ends']:
        assert data['ends'] > data['start']
        if today >= data['ends']:
            return False
    return data['start'] <= today


def date_as_string(o):
    """
    Zum Vergleich von datetime.date- und DateTime-Objekten

    >>> standardbeast = date(2016, 1, 16)
    >>> date_as_string(standardbeast)
    '2016/01/16'
    >>> plonebeast = DateTime(DateTime('2015/12/30 00:00:00 GMT+0'))
    >>> date_as_string(plonebeast)
    '2015/12/30'
    >>> date_as_string(standardbeast) > date_as_string(plonebeast)
    True
    >>> date_as_string(12345)
    Traceback (most recent call last):
      ...
    ValueError: Can't convert <type 'int'> 12345
    """
    if not o:
        return ''
    if isinstance(o, date):
        return o.strftime('%Y/%m/%d')
    if isinstance(o, DateTime):
        return o.Date()
    raise ValueError("Can't convert %s %r"
                     % (type(o), o))


if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()

# vim: ts=8 sts=4 sw=4 si et
