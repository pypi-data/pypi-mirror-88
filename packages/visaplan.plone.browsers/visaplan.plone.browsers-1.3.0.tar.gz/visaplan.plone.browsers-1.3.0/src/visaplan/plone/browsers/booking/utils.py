# -*- coding: utf-8 -*- äöü
"""
utils-Modul des Browsers unitracc@@booking

Autor: Tobias Herp
"""
# Python compatibility:
from __future__ import absolute_import

from six.moves import map, range

# Standard library:
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from hashlib import md5

# Zope:
from Products.MailHost.MailHost import MailHostError

__all__ = ['sendMail',
           'extract_float',
           'paypal_langcode',
           'article_dicts',
           'moneyfmt',  # Beispiel von <https://docs.python.org/2/library/decimal.html#recipes>,
           'MF_KWARGS', # zum Aufruf von moneyfmt
           'format_decimal',  # ähnlich moneyfmt
           'extract_pretty_currency',
           ]
# visaplan:
from visaplan.plone.tools.context import getActiveLanguage
from visaplan.tools.coding import safe_decode
from visaplan.tools.minifuncs import translate_dummy as _

# Local imports:
from .data import \
    VAT_PERCENTAGE  # TODO: evtl. datumsabhängig in Datenbank ablegen
from .data import DD_MM_YYYY
from .exceptions import (
    BookingProgrammingError,
    MissingFallbackError,
    MissingValueError,
    MixedCurrencyException,
    MixedVendorException,
    UidNotfoundException,
    )

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import log_or_trace

gls_kwargs = {
    'defaultFromDevMode': 0,
    }
logger, debug_active, DEBUG = getLogSupport(**gls_kwargs)
lot_kwargs = {'debug_level': debug_active,
              'logger': logger,
              'log_result': True,
              'log_args': True,
              }

# -------------------------------------------- [ Daten ... [
# (hier definiert wg. Doctests; siehe auch ./data.py)
PAYPAL_KNOWN_LANGCODES = {'de': 'de_DE',
                          'en': 'en_US',
                          'es': 'es_ES',
                          }
for val in PAYPAL_KNOWN_LANGCODES.values():
    PAYPAL_KNOWN_LANGCODES[val] = val
try:
    # visaplan:
    from visaplan.tools.html import entity
    EUROSIGN = entity['euro']
    HARDSPACE = entity['nbsp']
    # Local imports:
    from .data import PAYPAL_KNOWN_CURRENCYCODES
except (ValueError, ImportError):  # Testbarkeit
    EUROSIGN = u'\u20ac'
    HARDSPACE = u'\xa0'
    PAYPAL_KNOWN_CURRENCYCODES = ['EUR', 'USD']

# TODO: init-Funktion erstellen
PAYPAL_CURRENCYCODE = {}
for code in PAYPAL_KNOWN_CURRENCYCODES:
    PAYPAL_CURRENCYCODE[code] = code
for code in ('US$', '$'):
    PAYPAL_CURRENCYCODE[code] = 'USD'
for code in (EUROSIGN, u'Euro'):
    PAYPAL_CURRENCYCODE[code] = 'EUR'

PRETTY_CURRENCY = {
    'USD': u'US$',
    'EUR': EUROSIGN,
    }
DEFAULT_CURRENCYCODE = 'EUR'
assert DEFAULT_CURRENCYCODE in PAYPAL_KNOWN_CURRENCYCODES


# ----------------------------------------------- [ für sendMail ... [
# ---------------------------------------- [ für den Parser ... [
MAIL_MSG = ((_('Sent mail from ${mail_from} to ${mail_to}'), #  [0][0]
             _('Sent mail from ${mail_from} to ${mail_to}'   #  [0][1]
               ', subject: ${subject}'),
             ),
            (_('Error sending mail'                          #  [1][0]
              ' from ${mail_from} to ${mail_to}'),
             _('Error sending mail'                          #  [1][1]
              ' from ${mail_from} to ${mail_to}'
              ', subject: ${subject}'),
             ))
del _  # --------------------------------- ] ... für den Parser ]
# dasselbe nochmal für Logging (nicht zu übersetzen):
MAIL_LOG = (('Sent mail from %(mail_from)r to %(mail_to)r', #  [0][0]
             'Sent mail from %(mail_from)r to %(mail_to)r'  #  [0][1]
             ', subject: %(subject)r',
             ),
            ('Error sending mail'                           #  [1][0]
             ' from %(mail_from)r to %(mail_to)r',
             'Error sending mail'                           #  [1][1]
             ' from %(mail_from)r to %(mail_to)r'
             ', subject: %(subject)r',
             ))
# ----------------------------------------------- ] ... für sendMail ]
NONCURRENCY_CHARS = set(u' \t\n\r.,:;\\\'"-/0123456789' + HARDSPACE)
# -------------------------------------------- ] ... Daten ]


def _generate_currency_candidates(s):
    """
    Hilfsfunktion für extract_currency und (indirekt) extract_pretty_currency
    """
    buf = []
    currency_active = False
    for ch in safe_decode(s):
        is_currsign = ch not in NONCURRENCY_CHARS
        if is_currsign:
            buf.append(ch)
            currency_active = True
        elif currency_active:
            currency_active = False
            yield u''.join(buf)
            del buf[:]
    if buf:
        yield u''.join(buf)


def extract_currency(s):
    """
    Extrahiere die Währungsangabe aus einer Zeichenkette

    >>> extract_currency(u'80€ / Monat')
    'EUR'
    >>> extract_currency(u'US$')
    'USD'
    >>> extract_currency('')
    """
    buf = []
    currency_active = False
    for curr in _generate_currency_candidates(s):
        try:
            return PAYPAL_CURRENCYCODE[curr]
        except KeyError:
            pass


def extract_pretty_currency(s):
    """
    Extrahiere die Währungsangabe aus einer Zeichenkette

    >>> extract_pretty_currency(u'80€ / Monat')
    u'\u20ac'
    >>> extract_pretty_currency(u'USD')
    u'US$'
    >>> extract_pretty_currency('')
    """
    pp_cc = extract_currency(s)
    if pp_cc is None:
        return pp_cc
    try:
        return PRETTY_CURRENCY[pp_cc]
    except KeyError:
        return pp_cc


@log_or_trace(**lot_kwargs)
def sendMail(mail, mail_from, mail_to,
             message=None,
             # alle folgenden stets benannt angeben:
             success_msg=None,
             error_msg=None,
             mapping={},
             **kwargs):
    """
    Sende eine Mail und gib True (im Erfolgsfall) oder False zurück.

    mail -- context.getBrowser('unitraccmail'). Da ohnehin vor dem Aufruf
            manipuliert, hier zu übergeben.
    mail_from, mail_to -- die an mail.sendMail übergebenen Argumente

    Optional (wenn nicht übergeben, gibt es keine Flash-Message):
    message -- der "message-Adapter"
               (bzw. eine entsprechende von getMessenger erzeugte Funktion),
               zur Ausgabe einer Flash-Message

    Die folgenden sollen *immer* benannt übergeben werden:

    success_msg -- Nachrichtentext zur Ausgabe als Flash-Message
    error_msg -- Nachrichtentext zur Ausgabe als Flash-Message
                 im Fehlerfall
    mapping -- ein dict zur Textersetzung für Logging und etwaige
               Flash-Messages, z. B. locals().
               Wenn übergeben, werden etwaige **kwargs ignoriert.

    """
    if not mapping:
        mapping = {'mail_from': mail_from,
                   'mail_to':   mail_to,
                   }
        mapping.update(kwargs)
    try:
        mail.sendMail(mail_from, mail_to)
    except MailHostError as e:
        if error_msg != 0 and message is not None:
            if error_msg is None:
                error_msg = MAIL_MSG[1]['subject' in mapping]
            message(error_msg,
                    mapping=mapping,
                    messageType='error')
        logger.error(MAIL_LOG[1]['subject' in mapping], mapping)
        logger.exception(e)
        return False
    else:
        if success_msg != 0 and message is not None:
            if success_msg is None:
                success_msg = MAIL_MSG[0]['subject' in mapping]
            message(success_msg,
                    mapping=mapping,
                    messageType='info')
        logger.info(MAIL_LOG[0]['subject' in mapping], mapping)
        return True


def make_secret(order_id):
    """
    vorerst die simple Variante wie bisher;
    perspektivisch eine generierte Funktion, die z. B. ein konfiguriertes Seed verwendet
    """
    return md5(str(order_id)).hexdigest()

def extract_float(s):
    """
    Extrahiere eine Zahl aus einem String, der eine Währungsangabe enthält.

    >>> extract_float('600,00 &euro;')
    600.0

    Wenn der übergebene Wert bereits eine Zahl ist,
    gib ihn unverändert zurück:
    >>> extract_float(600.0)
    600.0
    """
    if isinstance(s, (float, int, Decimal)):
        return s
    if not s:
        raise ValueError("Can't extract float from %(s)r"
                         % locals())
    for subs in s.split():
        try:
            if ',' in subs:
                return float(subs.replace(',', '.'))
            else:
                return float(subs)
        except ValueError:
            pass
    raise

def float_to_euro(num):
    """
    Formatiere eine "Fließkommazahl" als Euro-Betrag

    >>> float_to_euro(123.45)
    u'123,45 \u20ac'

    Es findet vorerst noch keine Tausender-Gruppierung statt.
    """
    return (u'%.2f \u20ac' % num).replace('.', ',')


def paypal_langcode(code):
    """
    Nimm einen Sprachcode entgegen und gib eine Version zurück,
    für die PayPal einen Buy-Now-Button im Repertoire hat

    >>> paypal_langcode('de')
    'de_DE'
    >>> paypal_langcode('en')
    'en_US'
    >>> paypal_langcode('en_US')
    'en_US'
    >>> paypal_langcode('ru')
    'ru_RU'
    """
    try:
        return PAYPAL_KNOWN_LANGCODES[code]
    except KeyError:
        liz = code.split('_', 1)
        co1 = liz[0]
        if len(co1) == 2:
            return '_'.join((co1, co1.upper()))
        else:
            return 'en_US'


def normal_currency(currency):
    if currency is None:
        return None
    return PRETTY_CURRENCY[PAYPAL_CURRENCYCODE[currency]]


def make_amount_formatter(currency, comma=None):
    """
    Gib eine Formatierungsfunktion zurück, die (als Zahl oder String)
    übergebene Beträge um die Währungsangabe ergänzt.

    Die Standardwährung ist der Euro;
    Eurobeträge werden mit Dezimalkomma ausgegeben:

    >>> f = make_amount_formatter(None)
    >>> f('1.2')
    u'1,20 \u20ac'

    Dollarbeträge werden mit Dezimalpunkt ausgegeben:
    >>> f2 = make_amount_formatter('$')
    >>> f2('123.4')
    u'123.40 US$'
    """
    if not currency:
        currency = DEFAULT_CURRENCYCODE
    pretty_currency = PRETTY_CURRENCY[PAYPAL_CURRENCYCODE[currency]]
    assert u'.' not in pretty_currency  # wg. etwaiger Ersetzung
    # erstmal: EUR-Beträge nach deutscher Konvention formatieren,
    #          Dollarbeträge nach US-Konvention
    if comma is None:
        if PAYPAL_CURRENCYCODE[pretty_currency] == 'EUR':
            comma = u','
    elif not comma:
        comma = None

    def simple_formatter(amount):
        return u'%.2f %s' % (float(amount or 0), pretty_currency)

    def comma_formatter(amount):
        return simple_formatter(amount).replace(u'.', comma)

    if comma is None:
        return simple_formatter
    else:
        return comma_formatter


def article_dicts(uid, order, hub, info,  # ---- [ article_dicts ... [
                  quantity=1):
    """
    Erstelle ein Python-Dict, um den Artikel mit der übergebenen UID
    der Tabelle unitracc_orders_articles hinzuzufügen;
    außerdem wird ein Dict zur etwaigen Aktualisierung des order-Dicts
    zurückgegeben:

    >>> article, update = article_dicts(uid, order, hub, info)
    """
    o = hub['rc'].lookupObject(uid)

    if o is None:
        raise UidNotfoundException(uid)

    order_id = order['order_id']
    # article_title = o.pretty_title_or_id()
    article_title = o.Title() or o.getId()

    order_update = {}

    # Währung:
    article_currency = o.getPrice_currency() or None
    if article_currency is None:
        val = o.getPrice()
        if val:
            article_currency = extract_currency(val)
    if article_currency is None:
        article_currency = DEFAULT_CURRENCYCODE
    order_currency = order.get('currency')
    if order_currency:
        oldval = normal_currency(order_currency)
        newval = normal_currency(article_currency)
        if newval != oldval:
            raise MixedCurrencyException(article_title, oldval, newval)
    else:
        order_update['currency'] = order_currency = article_currency

    # PayPal-Zahlung erlaubt?
    article_paypal_allowed = o.getPaypal_allowed()
    if not article_paypal_allowed:
        order_update['paypal_allowed'] = False

    # Anbieter bzw. PayPal-ID:
    article_paypal_id = o.getPaypal_id()
    if article_paypal_id:
        oldval = order.get('paypal_id')
        if oldval:
            if (article_paypal_id != oldval):
                raise MixedVendorException(article_title, oldval, article_paypal_id)
        else:
            order_update['paypal_id'] = article_paypal_id

    # Mehrwertsteuer (MwSt) / VAT:
    article_vat = o.getPrice_vat()
    price_shop = o.getPrice_shop()  # Der Zahlenwert
    vat_percent = o.getPrice_vat()
    if vat_percent is None or vat_percent == '':
        vat_percent = VAT_PERCENTAGE * 100
    else:
        if 0 < vat_percent < 1:
            raise ValueError('price_vat ist < 1 - Multiplikation notwendig!'
                             ' (%(o)r, %(vat_percent)r)'
                             % locals())
        assert vat_percent >= 0, (
            'Negative Umsatzsteuer ist eher nicht zu erwarten'
            ' (%(o)r, %(vat_percent)r)'
            ) % locals()

    # ------------------------ [ Reparaturcode ... [
    try:
        shopduration = o.getShopduration()
    except AttributeError as e:
        logger.error("Can't get shopduration of %(o)r!", locals())
        logger.exception(e)
        # hier gibt es noch ein Problem:
        if IUnitraccEntity.providedBy(o):
            la = getActiveLanguage(o)  # oder context
            if la == 'de' or la.startswith('de_'):
                shopduration = 731
            elif la == 'en' or la.startswith('en_'):
                shopduration = 366
            else:
                raise MissingFallbackError(article_title, 'shopduration', la)
            logger.warn("Set fallback 'shopduration' value to %(shopduration)r (language=%(la)r)",
                        locals())
        else:
            raise BookingProgrammingError(title=article_title)
    # ------------------------ ] ... Reparaturcode ]

    if not price_shop:
        raise MissingValueError(article_title, 'price_shop')
    if not shopduration:
        raise MissingValueError(article_title, 'shopduration')

    price = extract_float(price_shop)
    logger.info('uid=%(uid)r, article_title=%(article_title)r, '
                'price_shop=%(price_shop)r, price=%(price)r', locals())

    group_id = o.getAssociatedGroup()
    if not group_id:  # ohne Gruppenverknüpfung: nicht buchbar!
        raise MissingValueError(article_title, 'group_id')
    discount_group = o.getDiscountGroup()
    if discount_group is None:
        logger.warn('No discount group for %(o)r', locals())

    article = {
        'article_uid':   uid,
        'article_title': article_title,
        'amount':        price,
        'duration':      shopduration,  # von Artikelobjekt, oder Fallback
        'order_id':      order_id,
        'quantity':      quantity,
        'vat_percent':   vat_percent,
        'group_id':      group_id,
        'discount_group': discount_group,
        }
    start = info['request_var'].get('start')
    if start:
        article['start'] = datetime.strptime(start, DD_MM_YYYY)
    return article, order_update
    # ------------------------------------------ ] ... article_dicts ]


def in_cart(articles):
    """
    Gib ein defaultdict und ein set zurück
    """
    articles_in_cart = {}
    for item in articles:
        articles_in_cart[item['article_uid']] = item['quantity']
    quantity = defaultdict(lambda: None)
    quantity.update(articles_in_cart)
    articles_in_cart = set(articles_in_cart.keys())
    return quantity, articles_in_cart


# Formatierungsfunktion von <https://docs.python.org/2/library/decimal.html#recipes>:
def moneyfmt(value, places=2, curr='', sep=',', dp='.',
             pos='', neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    places:  required number of places after the decimal point
    curr:    optional currency symbol before the sign (may be blank)
    sep:     optional grouping separator (comma, period, space, or blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: '+', space or blank
    neg:     optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator:  '-', ')', space or blank

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'

    """
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = list(map(str, digits))
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))


def format_decimal(value, places=2, **kwargs):
    """
    Formatiere eine Dezimalzahl, in Anlehnung an moneyfmt, mit folgenden Unterschieden:
    - alle Argumente außer dem Wert und der Anzahl der Nachkommastellen
      (Vorgabe: 2) müssen benannt angegeben werden
    - Das Währungssymbol wird stets hinten angehängt ...
    - ... und ggf. abgesetzt, per Vorgabe mit einem geschützten Leerzeichen

    >>> format_decimal(Decimal('19.0'), dp=',', curr='%', currsep='_')
    '19,00_%'

    Wenn places=None ist, werden nur die benötigten Kommastellen erzeugt:

    >>> format_decimal(Decimal('19.0'), places=None, curr='%', currsep='_')
    '19_%'
    """
    if places is None:
        sign, digits, exp = value.normalize().as_tuple()
    else:
        q = Decimal(10) ** -places      # 2 places --> '0.01'
        sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = list(map(str, digits))
    build, next = result.append, digits.pop
    opt = kwargs.pop
    if sign:
        build(opt('trailneg', ''))
    curr = opt('curr', '')
    if curr:
        build(curr)
        currsep = opt('currsep', HARDSPACE)
        if currsep:
            build(currsep)
    dp = opt('dp', '.')
    sep = opt('sep', None)
    if sep is None:
        if dp == '.':
            sep = ','
        else:
            sep = '.'
    assert dp != sep, ('dp %(dp)r and sep %(sep)r must be different!'
                       % locals())
    if places is None:
        if exp < 0:
            places = -exp
        else:
            places = 0
    for i in range(places):
        build(next() if digits else '0')
    if places > 0:
        build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    if sign:
        build(opt('neg', '-'))
    else:
        build(opt('pos', ''))
    return ''.join(reversed(result))


def all_user_names(row):
    names = []
    firstname = row.get('firstname')
    if firstname:
        names.append(firstname)
    lastname = row.get('lastname')
    if lastname:
        names.append(lastname)
    if names:
        tmp = ' '.join(names)
        del names[:]
        names.append(tmp)
    company = row.get('company')
    if company:
        names.append(company)
        tmp = ', '.join(names)
        del names[:]
        names.append(tmp)
    userid = row.get('userid')
    if names:
        names = ' '.join(names)
        return '%(names)s (%(userid)s)' % locals()
    else:
        return userid


# zum sprachspezifischen Aufruf von moneyfmt:
MF_KWARGS = defaultdict(lambda: {'sep': '.',
                                 'dp':  ',',
                                 })
MF_KWARGS['en_US'] = {'sep': ',',
                      'dp':  '.',
                      }
MF_KWARGS['en'] = MF_KWARGS['en_US']


if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()

# vim: ts=8 sts=4 sw=4 si et
