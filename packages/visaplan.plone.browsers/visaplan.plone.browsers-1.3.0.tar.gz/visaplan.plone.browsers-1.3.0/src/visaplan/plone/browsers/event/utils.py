# -*- coding: utf-8 -*- äöü
"""
Tools für den Browser @@event, ausgekoppelt zur Testbarkeit
"""

# Python compatibility:
from __future__ import absolute_import

# Standard library:
from copy import deepcopy
from datetime import date, datetime, timedelta
from time import strftime, strptime

# Local imports:
from .data import (
    DEFAULT_RANGE,
    GLEITENDE_WOCHE,
    GLEITENDER_MONAT,
    GLEITENDES_JAHR,
    GLEITENDES_QUARTAL,
    HEUTE,
    MANUAL_RANGE,
    NAECHSTE_10,
    PUBLIC_STATES,
    RANGE_CHOICES,
    )

# Logging / Debugging:
from logging import getLogger
from visaplan.tools.debug import pp

ONE_DAY = timedelta(days=1)
logger = getLogger(__package__)


def today_00():
    """
    >x> today_00()
    """
    return datetime.now().date()


def as_date(val):
    """
    Gib den übergebenen datetime.date- oder .datetime-Wert als datetime.date zurück
    """
    try:
        return val.date()
    except AttributeError:
        return val

    # das funzt leider nicht:
    if isinstance(val, date):
        return val
    return val.date()


def range_choices(choice):
    res = []
    append = res.append
    for key, val in RANGE_CHOICES:
        append({'value': key,
                'label': val,
                'selected': key == choice,
                })
    return res


def calc_range(choice, start=None):
    """
    Berechne das Enddatum aus dem Startdatum und dem angegebenen Typ;
    gib das (evtl. geänderte) Start- und das Enddatum zurück
    (stets als reines Datum, also mit Uhrzeit 0:00).

    Das start-Argument dient in erster Linie der Testbarkeit.

    >>> now = datetime(2015, 4, 27)

    Das "gleitende Quartal" beginnt am ersten des aktuellen Monats
    und endet drei Monate später (wiederum am ersten):

    >>> calc_range(GLEITENDES_QUARTAL, now)
    (datetime.date(2015, 4, 1), datetime.date(2015, 7, 1))
    >>> nikolaus = datetime(2015, 12, 6)
    >>> calc_range(GLEITENDES_QUARTAL, nikolaus)
    (datetime.date(2015, 12, 1), datetime.date(2016, 3, 1))
    """
    if start is None:
        start = datetime.now()

    if choice == GLEITENDES_QUARTAL:
        end = start_of_next_month(start, 3)
        start = start_of_next_month(start, 0)

    elif choice == GLEITENDES_JAHR:
        end = same_day_next_month(start, 12)

    # Heute und eine Woche
    elif choice in [HEUTE, GLEITENDE_WOCHE]:
        end = start+timedelta(days=int(choice))

    # naechste 10 Events; großzügiges Zeitlimit (2 Jahre):
    elif choice == NAECHSTE_10:
        end = same_day_next_month(start, 24)

    # naechster Monat
    elif choice == GLEITENDER_MONAT:
        end = same_day_next_month(start, 1)

    return as_date(start), as_date(end)


def manual_range(form, choice=HEUTE, mask='%d.%m.%Y'):
    """
    Wie calc_range, aber mit Angabe der Datumswerte per Formular
    (Schlüssel 'start' und 'end').  Wenn <end> fehlt, wird das
    <choice>-Argument verwendet und calc_range aufgerufen:

    >>> form = {'start': '27.4.2015'}
    >>> manual_range(form, GLEITENDER_MONAT)
    (datetime.date(2015, 4, 27), datetime.date(2015, 5, 27))

    Es gibt noch keine spezielle Logik für den Fall, daß nur ein End-, aber
    kein Startdatum angegeben ist.  Ist das Enddatum <heute>, wird die Suche
    daher üblicherweise ein leeres Ergebnis liefern.
    """
    start = form.get('start', None)
    end = form.get('end', None)
    try:
        if not start:
            start = datetime.now()
        else:
            start = strptime(start, mask)
            start = datetime(start[0], start[1], start[2])
        if not end:
            return calc_range(choice, start)
        else:
            end = strptime(end, mask)
            # Bei manueller Angabe ist das obere Ende *einschließlich* gemeint!
            end = datetime(end[0], end[1], end[2]) + ONE_DAY

        return as_date(start), as_date(end)
    except ValueError as e:
        logger.error('Error converting dates (start=%(start)r, end=%(end)r',
                     locals())
        logger.exception(e)
        raise


def reverse_range(choice, end):
    """
    Entsprechend calc_range, aber für den Fall, daß das Ende-, aber nicht das
    Anfangsdatum angegeben wurde.

    Die choice-Angaben werden sinngemäß übersetzt; das gleitende Quartal z. B.
    beinhaltet den aktuellen Monat als letzten, nicht als ersten:

    >>> now = datetime(2015, 4, 27)
    >>> reverse_range(GLEITENDES_QUARTAL, now)
    (datetime.date(2015, 2, 1), datetime.date(2015, 5, 1))

    >>> silvester = datetime(2015, 12, 31)
    >>> reverse_range(GLEITENDER_MONAT, silvester)
    (datetime.date(2015, 12, 1), datetime.date(2016, 1, 1))
    >>> reverse_range(GLEITENDER_MONAT, now)
    (datetime.date(2015, 3, 27), datetime.date(2015, 4, 28))
    """
    if choice == GLEITENDES_QUARTAL:
        start = start_of_next_month(end, -2)
        end = start_of_next_month(end, 1)
    else:
        if choice == GLEITENDES_JAHR:
            start = same_day_next_month(end, -12)

        # Heute und eine Woche
        elif choice in [HEUTE, GLEITENDE_WOCHE]:
            start = end + timedelta(days=1-choice)

        # naechste 10 Events; großzügiges Zeitlimit (2 Jahre):
        elif choice == NAECHSTE_10:
            start = same_day_next_month(end, -24)

        # naechster Monat
        elif choice == GLEITENDER_MONAT:
            test = end + ONE_DAY
            # am Ultimo mit dem Monatsersten beginnen:
            if test.day == 1:
                start = same_day_next_month(test, -1)
            else:
                start = same_day_next_month(end, -1)
            return as_date(start), as_date(test)
        # Angegebenes Ende ist immer einschließlich:
        end = end + ONE_DAY

    return as_date(start), as_date(end)


def query_dict(start, end,
               review_state=PUBLIC_STATES,
               portal_type='UnitraccEvent',
               sort_on='start',
               sort_order=None,  # oder 'ascending'?
               sort_limit=None):
    """
    Erzeuge das Query-Dict.

    >>> q = query_dict('START', 'END')
    >>> sorted(q.items())
    [('portal_type', 'UnitraccEvent'), ('review_state', ['inherit', 'published']), ('sort_on', 'start'), ('start', {'query': ('START', 'END'), 'range': 'min:max'})]
    >>> q['start']
    {'query': ('START', 'END'), 'range': 'min:max'}

    Die ersten beiden Argumente sind <start> und <end>; sie dürfen als None
    übergeben werden:

    >>> q1 = query_dict('START', None)
    >>> q1['start']
    {'query': 'START', 'range': 'min'}
    >>> q2 = query_dict(None, 'END')
    >>> q2['start']
    {'query': 'END', 'range': 'max'}

    Es wird standardmäßig nach Review-Status gefiltert:

    >>> 'review_state' in q2
    True

    Die Prüfung auf den Review-Status kann unterdrückt werden:

    >>> q3 = query_dict('START', 'END', review_state=None)
    >>> 'review_state' in q3
    False
    """
    res = {}
    if start is not None:
        if end is not None:
            res['start'] = {'query': (start, end),
                            'range': 'min:max',
                            }
        else:
            res['start'] = {'query': start,
                            'range': 'min',
                            }
    elif end is not None:
        res['start'] = {'query': end,
                        'range': 'max',
                        }
    for key in ('review_state', 'portal_type',
                'sort_on', 'sort_limit',
                ):
        val = locals()[key]
        if val is not None:
            res[key] = val
    return res


def shortened_query(dic, maxlen=3):
    """
    Gib ein nötigenfalls gekürztes und dann *nicht* äquivalentes Query-Dict zurück

    """
    res = deepcopy(dic)
    gCS = 'getCustomSearch'
    subdict = res.get(gCS, {})
    if subdict:
        ql = len(subdict['query'])
        if ql > maxlen:
            subdict['query'][maxlen-1:] = ['... (%d Eintraege)' % ql]
    return res


def start_of_next_month(now, delta=1):
    """
    Gib den ersten Tag des nächsten Monats zurück (delta=1):

    >>> now = datetime(2015, 4, 27)
    >>> start_of_next_month(now)
    datetime.date(2015, 5, 1)

    >>> nikolaus = datetime(2015, 12, 6)
    >>> start_of_next_month(nikolaus)
    datetime.date(2016, 1, 1)

    Mit 0 kommt der Erste des aktuellen Monats:
    >>> start_of_next_month(nikolaus, 0)
    datetime.date(2015, 12, 1)

    Mehr Monate in die Zukunft:
    >>> start_of_next_month(nikolaus, 15)
    datetime.date(2017, 3, 1)

    Es dürfen auch negative Werte angegeben werden:
    >>> start_of_next_month(now, -1)
    datetime.date(2015, 3, 1)
    >>> start_of_next_month(now, -12)
    datetime.date(2014, 4, 1)

    >>> neujahr = datetime(2015, 1, 1)
    >>> start_of_next_month(neujahr, -1)
    datetime.date(2014, 12, 1)
    """
    month = now.month
    year = now.year
    if delta > 0:
        dyear, dmonth = divmod(month+delta-1, 12)
        month = dmonth + 1
        year += dyear
    elif delta < 0:
        dyear, dmonth = divmod(month+delta, 12)
        month = dmonth
        year += dyear
        if month == 0:
            month = 12
            year -= 1
    return as_date(datetime(year, month, 1))


def same_day_next_month(now, delta=1):
    """
    >>> neujahr = datetime(2015, 1, 1)
    >>> same_day_next_month(neujahr, -1)
    datetime.date(2014, 12, 1)

    Klingt einfach: einfach den month-Wert ersetzen und ggf. das Jahr anpassen
    (was allerdings schon ein Grund für eine Funktion wäre) ...
    Die Anpassung des Monats kann aber fehlschlagen!

    >>> nikolaus = datetime(2015, 12, 6)
    >>> same_day_next_month(nikolaus, 1)
    datetime.date(2016, 1, 6)

    Negative Werte sind erlaubt:
    >>> same_day_next_month(nikolaus, -1)
    datetime.date(2015, 11, 6)

    >>> neujahr = datetime(2015, 1, 1)
    >>> same_day_next_month(neujahr, -1)
    datetime.date(2014, 12, 1)

    Im Notfall wird auf den Ultimo zurückgegriffen:

    >>> now = datetime(2015, 3, 31)
    >>> same_day_next_month(now, 1)
    datetime.date(2015, 4, 30)
    >>> silvester = datetime(2015, 12, 31)
    >>> same_day_next_month(silvester, -1)
    datetime.date(2015, 11, 30)

    Auch Schaltjahre werden implizit berücksichtigt:

    >>> feb29 = datetime(2016, 2, 29)
    >>> same_day_next_month(feb29, 12)
    datetime.date(2017, 2, 28)
    >>> same_day_next_month(feb29, -12)
    datetime.date(2015, 2, 28)
    >>> same_day_next_month(feb29, 48)
    datetime.date(2020, 2, 29)
    """
    month = now.month
    year = now.year
    day = now.day
    if delta > 0:
        dyear, dmonth = divmod(month+delta-1, 12)
        month = dmonth + 1
        year += dyear
    elif delta < 0:
        dyear, dmonth = divmod(month+delta, 12)
        month = dmonth
        year += dyear
        if month == 0:
            month = 12
            year -= 1
    try:
        # kann für keinen Dezember fehlschlagen ...
        return as_date(datetime(year, month, day))
    except ValueError:
        # ... also kann zum Monat gefahrlos addiert werden:
        return as_date(datetime(year, month+1, 1) - ONE_DAY)


if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()
