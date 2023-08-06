# -*- coding: utf-8 -*- äöü
"""
Browser unitracc@@booking

Ursprünglicher Autor:    Enrico Ziese;
Überarbeitung 2018 durch Tobias Herp

Neu:
- Verlagerung von Funktionalitäten in die Datenbank, soweit möglich:
  - Verwendung von Sichten
  - Verwendung von Triggerfunktionen
  - Verwendung von Vorgabewerten
  - Verwendung von "stored procedures" (recalculate_order)
- wichtige neue Methoden:
  - _get_order_articles_and_calculation - die Artikel des übergebenen Auftrags,
    mit Berechnung
  - _send_mail: universelle Versandmethode als Ersatz für die subtil
    unterschiedlichen Methoden _send_success_mail, _send_confirmation_mails etc.
    (NOCH UNFERTIG)

Indexfelder umbenannt:
unitracc_orders.id               --> order_id
unitracc_orders_articles.orderid --> order_id
unitracc_orders_articles.id      --> article_id

Verweise auf Hilfstabellen geändert:
unitracc_orders.payment_type   --> payment_type
unitracc_orders.booking_states_id --> booking_state

Lesen aus Hilfstabellen über neue Sichten, ohne id-Feld:
unitracc_payment_types  --> payment_types_view
unitracc_booking_states --> booking_states_view


Methoden:

Name                                Auftrag      Artikel   berechnet Anmerkungen
_get_current_order                  existierend  nein      nein
_get_orders                         existierende
                                    (eine Liste)
_get_order                          existierend
get_order                           ja           nein      nein
_get_or_create_order                                                   Hilfsfunktion für get_order
get_complete_order_info_by_order_id existierend  ja        ja          ruft _get_order und _get_order_articles_and_calculation auf
get_existing_order                  existierend  ja        (ja)
                                    oder Dummy

Außerdem:
_delete_order  löscht nach order_id Aufträge, Artikel und Gruppenzuordnungen
"""

# Python compatibility:
from __future__ import absolute_import, print_function

from six import string_types as six_string_types
from six.moves import map

__author__ = "enrico"
__date__ = "$05.09.2013 13:57:10$"

# Standard library:
from datetime import date, datetime, timedelta
from decimal import Decimal
from operator import attrgetter

# Zope:
from AccessControl import Unauthorized
from App.config import getConfiguration
from DateTime import DateTime
from zExceptions import Forbidden, Redirect

# 3rd party:
import pytz
from psycopg2 import IntegrityError, ProgrammingError

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.groups.unitraccgroups.utils import learner_group_id
from visaplan.plone.tools.context import \
    message  # requires context 1st argument
from visaplan.plone.tools.context import getMessenger

try:
    # visaplan:
    from visaplan.plone.unitracctool.unitraccfeature.utils import AGB_UID
except ImportError:
    AGB_UID = None

# Zope:
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.infohubs import make_hubs
from visaplan.plone.tools.context import make_timeFormatter, make_translator
from visaplan.plone.tools.forms import back_to_referer, tryagain_url
from visaplan.tools.classes import WriteProtected
from visaplan.tools.dicts import subdict, subdict_forquery, updated

# Local imports:
from .data import OLD2NEW_STATUS  # für Übergang
from .data import PAYPAL2UNITRACC_STATUS  # direkt textuelle Angabe
from .data import \
    VAT_PERCENTAGE  # TODO: evtl. datumsabhängig in Datenbank ablegen
from .data import (
    ACCEPTED_OR_BETTER,
    ACTIVE_VALUES,
    AUTHOR_BRAIN_TO_DB,
    DD_MM_YYYY,
    PAYPAL_PAYMENT_STATES,
    REQUIRED_FIELDS,
    TIMEOUT_MSGID,
    UNTOUCHED_ORDER_WHERE,
    USER_MAIL_SUBJECT,
    )
from .exceptions import BookingConfigurationError, UnitraccBaseException
from .utils import \
    article_dicts  # Formatierung von Geldbeträgen; als nächstes für insert_backend_booking
from .utils import (
    DEFAULT_CURRENCYCODE,
    MF_KWARGS,
    all_user_names,
    extract_float,
    format_decimal,
    in_cart,
    make_amount_formatter,
    make_secret,
    normal_currency,
    paypal_langcode,
    sendMail,
    )

# Logging / Debugging:
from pdb import set_trace
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import log_or_trace, pp

gls_kwargs = {
    'defaultFromDevMode': 0,
    }
logger, debug_active, DEBUG = getLogSupport(**gls_kwargs)
lot_kwargs = {'debug_level': debug_active,
              'logger': logger,
              'log_result': True,
              'log_args': True,
              }
# Standard library:
from pprint import pformat

# visaplan:
# ------------------------------------ [ Reparaturcode ... [
from Products.unitracc.content.interfaces import IUnitraccEntity
from visaplan.plone.tools.context import getActiveLanguage

# logger.info('UNTOUCHED_ORDER_WHERE=%(UNTOUCHED_ORDER_WHERE)s', globals())

# ------------------------------------ ] ... Reparaturcode ]


class IBooking(Interface):
    """
    Verantwortlich für alle Buchungsrelevanten Datenbankvorgänge
    """

    def get_backend_bookings():
        """
        Hole alle Buchungen für die Verwaltung
        """

    def get_user_bookings():
        """
        Hole alle Buchungen für die Verwaltung
        """

    def get_order_view(order_id):
        """
        Ermittle die Daten für die Bestellungsansicht (templates/order_view.pt)
        """

    def get_payment_types(type=None, tid=None):
        """
        Holt die Zahlungsarten (msgid: "Payment method") heraus.
        """

    def get_bookable_courses():
        """
        Filtere die vorhandenen Kurse danach, ob sie auch wirklich
        buchbar sind, d.h. einen Preis und eine Dauer haben
        """

    def get_current_order_articles():
        """
        gib die Artikel der aktuellen Bestellung wieder
        """

    def get_order(**kwargs):
        """
        Gib den für die aktuelle Session existierenden Bestellungs-Datensatz zurück;
        dieser wird ggf. zuvor erzeugt.
        """

    def add_article():
        """
        Füge den Artikel <uid> (aus Formulardaten) der Bestellung hinzu;
        wenn noch keine Bestellung vorhanden ist, erzeuge sie per Aufruf von  --> _insert_order.
        Anschließend Umleitung zur Ansicht der Bestellung.
        """

    def insert_backend_booking():
        """
        Annehmen der Formulardaten einer Buchung
        und Prozessierung der Speicherung
        """

    def delete_order():
        """
        Eine Bestellung aus dem System komplett löschen
        """

    def update_order_payment():
        """
        Aktualisieren des Payment Status
        """

    def edit_article():
        """
        Aktualisieren der Artikel zu einer Bestellung aus dem Backend
        """

    def edit_order():
        """
        Eine bestehende Bestellung editieren.
        """

    def edit_order_view(order_id):
        """
        Eine bestehende Bestellung editieren.
        """

    def delete_article():
        """
        Einen Artikel aus meiner Bestellung löschen.
        """

    def check_access(web=False):
        """
        Prüfe den Zugriff

        Erzeugt eine Formularvariable "formid".
        Die Methode ist wg. plone4.csrffixes mutmaßlich obsolet.
        """

    def process_cart():
        """
        Vom Warenkorb zur Kasse
        """

    def process_order_register():
        """
        Rechnungsdaten entgegenehmen und verarbeiten.
        """

    def submit_order():
        """
        annehmen und Abschicken der Bestellung
        """

    def can_view_booking_button(object_):
        """
        Bestimmt, ob der Buchungs-Button angezeigt werden soll
        """

    def save_payment():
        """
            Bezahlungsart speichern
        """

    def save_preferences(backend=False):
        """
        Formularaktion für --> templates/order_preferences.pt

        Ersetzt die alte Methode save_payment
        """

    def get_agb_link():
        """
            Gibt die URL der AGB Seite zurück.
        """

    def get_paypal_button(order):
        """
        Erzeuge den Jetzt-Kaufen-Button für PayPal (HTML)
        """

    def paypal_finished():
        """
            Rückantwortsmethode für Paypal.
            Speicherung der von Paypal übermittelten Daten
        """

    def get_complete_order_info_by_order_id(order_id):
        """
            Order, Artikel + Zusatzinfos
        """

    def get_paypal_payment_states():
        """
            Gibt Payopal Payment status zurück + Erläuterung
        """

    def get_paypal_history_by_order_id(order_id):
        """
            PayPal-Historie aus der Datenbank
        """

    def get_paypal_urls():
        """
        Gib die Liste der erlaubten PayPal-URLs zurück
        """

    def get_sending_mail_address(config=None):
        """
        Ermittle die sendende Mail-Adresse (Subportal-Eigenschaft)
        """

    def make_greeting(order):
        """
        order - ein dict (Datensatz aus `unitracc_orders`)
        """


class Browser(BrowserView):
    """
    """
    implements(IBooking)

    config_storage_key = 'booking'

    def __init__(self, context, request):
        """
        """
        BrowserView.__init__(self, context, request)
        # TODO: - self.sql eliminieren
        #       - stattdessen Kontextmanager-Protokoll verwenden
        #         (with ...getAdapter('sqlwrapper') as sql:)
        #         und das sql-Objekt ggf. übergeben
        #       - noch besser: direkt den Datenbank-Cursor verwenden
        #         (neuer Adapter dbcursor)
        self.sql = self.context.getAdapter('sqlwrapper')

    # @log_or_trace(**lot_kwargs)
    def get_backend_bookings(self):  # -- [ get_backend_bookings ... [
        """
        Verwendung: Zuweisung in templates/order_management.pt

        Hole alle Buchungen für die Verwaltung

        TODO:
        - gegenwärtig 6 SQL-Aufrufe für unterschiedliche Statuus -> einer reicht!
        - möglichst auch die bestellten Artikel in derselben Query erschlagen
        - Klartext-Information über Zahlungsstatus
        """
        context = self.context
        totime = make_timeFormatter(context)

        with self.sql as sql:
            result = {'new':    [], # noch nicht bezahlt
                      'paid':   [], # bezahlt (vormals 'payed')
                      'failed': [], # fehlgeschlagene Buchungen
                      'other':  [], # sonstiges (vor März 2018 nicht ausgegeben)
                      }
            result['all'] = self._get_orders(sql)

            for row in result['all']:

                if row['ordernr'] is not None:
                    cat = row['payment_status_category']
                else:
                    cat = 'other'  # oder ignorieren?
                # lokalisierte Zeitangaben, lang:
                row['date_payed'] = totime(row['date_payed'], 1)
                row['date_booked'] = totime(row['date_booked'], 1)
                row['articles'] = list(sql.select('orders_articles_view',
                                                  query_data={'order_id': row['order_id'],
                                                              'step': 1,
                                                              }))
                row['all_names'] = all_user_names(row)
                asm = row['access_settlement_mode']
                if asm:
                    row['asm_msgid'] = 'access_settlement_mode_' + asm
                else:
                    row['asm_msgid'] = None
                # Änderung der Schlüssel im März 2018:
                # 'real_start' (unitracc_groupmemberships.start) --> 'start_ddmmyyyy'
                # 'real_end'   (unitracc_groupmemberships.ends)  --> 'ends_ddmmyyyy'
                result[cat].append(row)
            # vormaligen Schlüssel erstmal noch unterstützen:
            result['payed'] = result['paid']

        return result
        # ------------------------------- ] ... get_backend_bookings ]

    # @log_or_trace(**lot_kwargs)
    def get_user_bookings(self, status=None):
        """
        Verwendung: Zuweisung in ../../skins/unitracc_templates/group-desktop.pt

        Hole alle Buchungen für die Useransicht
        status -- optionaler String; TH: wird nicht verwendet

        Siehe neue SQL-View user_bookings_view:
        - start und ends aus unitracc_groupmemberships sind enthalten
          (macht _get_access_duration überflüssig):
          - als Datumswerte (start, ends)
          - formatiert als dd.mm.yyyy (start_ddmmyyyy, ends_ddmmyyyy)
        - unitracc_booking_states.booking_state als payment_status
          (macht _get_booking_status überflüssig.
          Wird die booking_states_id benötigt?)
        - payment_type und payment_type
          (macht _get_payment_types überflüssig)
        """
        hub, info = make_hubs(self.context)
        with self.sql as sql:
            self._delete_expired_order(sql)
            user_id = info['user_id']
            is_member_of = info['is_member_of']

            orders = self._get_orders(sql,
                                      userID=user_id,
                                      payment_status=sorted(ACCEPTED_OR_BETTER))
            # davon gibt es meist nicht viele:
            for order in orders:
                order_id = order['order_id']
                articles = order['articles'] = list(sql.select(
                    'orders_articles_view',
                    query_data={'order_id': order_id,
                                }))
                for article in articles:
                    uid = article['article_uid']
                    group_id = article['group_id']
                    article['article_path'] = (
                        uid and group_id
                        and is_member_of(group_id)
                        and info['uid2path'][uid]
                        or None)
        return orders

    # @log_or_trace(**lot_kwargs)
    def get_current_order_articles(self, sql=None, complete=None):
        """
        Verwendung: in ...
        - templates/mycart.pt
        - templates/checkout.pt
        - templates/order_choose_payment_method.pt
        - templates/order_overview.pt

        Gib die aktuelle Bestellung incl. der Artikel wieder;
        der Rückgabewert (mit complete=True) wird an get_paypal_button übergeben

        Siehe neue SQL-View: orders_articles_view

        Achtung, das complete-Argument muß beim Aufruf aus Seitentemplates ggf.
        benannt übergeben werden!
        """
        pm = getToolByName(self.context, 'portal_membership')
        if pm.isAnonymousUser():
            raise Unauthorized
        if sql is not None:
            return self._get_current_order_articles(sql, complete)
        with self.sql as sql:
            return self._get_current_order_articles(sql, complete)

    def _get_current_order_articles(self, sql, complete=None):

        order = self._get_current_order(sql, complete)
        return self._get_order_articles_and_calculation(sql, order=order)

    def get_current_order_and_choices(self):
        """
        Gib die aktuelle Bestellung zurück, zzgl. der Auswahlen für Zahlungs- und Erledigungsart
        """
        pm = getToolByName(self.context, 'portal_membership')
        if pm.isAnonymousUser():
            raise Unauthorized
        hub, info = make_hubs(self.context)
        with self.sql as sql:
            return self._get_current_order_and_choices(sql, hub, info,
                                                       silent=False,
                                                       complete=True)

    def _get_current_order_and_choices(self, sql, hub, info,
                                       # bitte stets benannt übergeben:
                                       silent=False, backend=False,
                                       complete=0):
        result = self._get_current_order_articles(sql, complete=complete)

        articles = result['articles']
        order = result['order']
        if order is None:
            hub['message'](TIMEOUT_MSGID, 'error')
            raise Redirect('/mycart')
        choices = result['choices'] = {}

        # --------------------- direkte Freigabe oder TAN-Verfahren?
        current_settlement_mode = order['access_settlement_mode']
        direct_activation_possible = True
        pc = hub['portal_catalog']._catalog
        # pc = getToolByName(context, 'portal_catalog')._catalog
        for item in articles:
            if item['quantity'] > 1:
                direct_activation_possible = False
                break
            uid = item['article_uid']
            brains = pc(UID=uid)  # gibt LazyMap zurück, eine Art Liste
            if not brains:
                logger.warn('_get_current_order_and_choices: UID %(uid)r nicht gefunden!',
                            locals())
                continue
            brain = brains[0]
            if brain.portal_type == 'UnitraccEntity':
                direct_activation_possible = False
                break
        if (not silent
            and not direct_activation_possible
            and current_settlement_mode == 'immediate'
            ):
            hub['message']('Since your order involves access for more '
                           'than one user, immediate access settlement '
                           'is not possible.',
                           'error')
        choices['access_settlement_mode'] = settlement_mode_choices = []
        has_sm_selection = False
        for item in sql.select('access_settlement_modes_user_view'):
            mode_key = item['mode_key']
            if mode_key == 'immediate' and not direct_activation_possible:
                continue
            if mode_key == current_settlement_mode:
                has_sm_selection = True
                item['selected'] = True
            else:
                item['selected'] = False
            settlement_mode_choices.append(item)
        if not settlement_mode_choices:
            logger.error('XXX No settlement_mode_choices!')
        elif not has_sm_selection:
            item = settlement_mode_choices[0]
            item['selected'] = True
            logger.info('Auto-selected access_settlement_mode %(mode_key)r',
                        item)

        # --------------------------------------------- Zahlungsart?
        current_payment_type = order['payment_type']
        choices['payment_type'] = payment_type_choices = []
        disable_paypal = False
        paypal_found = False
        for item in sql.select('payment_types_view',
                               query_data={'active': ACTIVE_VALUES[backend],
                                           }):
            type_key = item['payment_type']
            if type_key == 'paypal':
                paypal_found = True
                if not self.check_paypal_setup():
                    disable_paypal = True
                    if backend:
                        # wie in alter Methode _get_active_payment_types:
                        item['disabled'] = 'setup incomplete'
                    else:
                        continue
            item['selected'] = type_key == current_payment_type
            payment_type_choices.append(item)

        return result

    def _get_user_and_session(self,  # - [ _get_user_and_session ... [
                              hub=None, info=None,
                              context=None,
                              return_context=None):
        """
        Ermittle die Benutzer- und die Session-ID und gib sie zurück.
        Der Rückgabewert ist, je nach Aufruf, ein 2-Tupel (user_id, session_id)
        oder ein 3-Tupel (context, user_id, session_id)

        Wenn ohnehin mit hub und info gearbeitet wird, ist es sinnvoll, diese
        vor dem Aufruf dieser Methode zu erzeugen und zu übergeben.
        """
        if hub is None:
            if context is None:
                if return_context is None:
                    return_context = True
                context = self.context
            hub, info = make_hubs(context)
        user_id = info['user_id']
        session_id = info['request']['SESSION'].getId()
        assert hub['member'].getId() == user_id
        if return_context:
            if context is None:
                context = info['context']
            return (context, user_id, session_id)
        return (user_id, session_id)  #
        # ------------------------------ ] ... _get_user_and_session ]

    # @log_or_trace(trace=0, **lot_kwargs)
    def _get_current_order(self, sql, complete=None):
        """
        Gib die Bestellung (den Einkaufswagen, ohne seinen Inhalt)
        des aktuell angemeldeten Benutzers zurück

        complete -- wenn True, wird die "XSS-Prüfung" durchgeführt
        """
        if complete:
            hack = self.check_access(True)
            if hack:
                return hack

        user_id, session_id = self._get_user_and_session(context=self.context)
        order = self._get_order(sql, payment_status='new',
                                sessionID=session_id,
                                userID=user_id)
        return order  # _get_current_order

    # @log_or_trace(trace=0, **lot_kwargs)
    def _get_order_articles_and_calculation(self,  # -- [ _goaac ... [
            sql,
            order=None, order_id=None):
        """
        Ermittle:
        - die aktuelle Bestellung (eine Zeile aus unitracc_orders);
          wenn nicht die order_id oder das komplette Dict übergeben,
          wird nach einer Bestellung mit Status 'new' für den aktuell angemeldeten Benutzer
          gesucht (--> _get_current_order)
        - den aktuellen Inhalt des Einkaufswagens ('art', für "articles")
        - die berechneten Zeilen für Rabatt und Mehrwertsteuer ('calc';
          macht _calculate_prices obsolet)

        Beim Aufruf wird <sql> übergeben.

        Siehe auch:
        - _get_current_order_and_choices
        """
        # dirty: "recalculate_order(order_id)" wird die Berechnungszeilen neu
        #        erstellen (und unitracc_orders aktualisieren)
        dirty = None
        check_user = False
        if order_id is None:
            if order is None:
                order = self._get_current_order(sql)
            if order is not None:
                order_id = order['order_id']
        else:
            check_user = True
        if order is not None:
            dirty = order['dirty']
            if check_user:
                hub, info = make_hubs(self.context)
                if (order['userid'] != info['user_id']
                    and not info['has_perm']['Manage portal']
                    ):
                    raise Forbidden("You don't exist. Go away.")

        articles = []
        calculated = []
        meta = {'display_quantity': False,
                'vat_column': False,
                'snippet': {},  # --> templates/booking_macros2.pt
                }
        result = {
            'order':      order,  # incl. 'currency'
            'articles':   articles,
            'meta':       meta,
            # berechnete Felder:
            'calculated': calculated,
            }

        if order is None:
            return result

        # für Mailversand:
        val = order['access_settlement_mode']
        if val is not None:
            meta['snippet']['after-payment'] = (
                    val == 'immediate'
                    and 'snippet-awaiting-course-payment'
                    or  'snippet-awaiting-payment-' + val)

        query_data = {'order_id': order_id,
                      }

        articles.extend(sql.select('articles_items_view',
                                   query_data=query_data))
        if not articles:
            return result

        # brauchen wir eine Spalte für die Anzahl?
        for row in articles:
            if row['quantity'] != 1:
                meta['display_quantity'] = True
                break

        context = self.context
        if order['la'] is None:
            # wichtig für die Funktion "recalculate_order":
            updated = list(sql.update('unitracc_orders',
                                      {'la': getActiveLanguage(context)},
                                      query_data=query_data,
                                      returning='la'))
            # die Datenbank ersetzt 'de' --> 'de_DE' etc.:
            order.update(updated[0])

        calculated.extend(sql.query('select * from '
                                    'recalculate_order(%(order_id)s);',
                                    query_data=query_data))
        #changes = WriteProtected()
        changes = {}
        # für den Übergang (alten Code unterstützen):
        # changes['order_id'] = order['order_id']

        if dirty:
            vat_sum = Decimal(0)
            # datenbankseitig ist das nun durch recalculate_order erledigt,
            # aber die alten Werte aus _get_current_order sind noch nicht verläßlich:
            for row in calculated:
                step = row['step']
                if step == 7:
                    changes['net_total'] = row['amount_multiplied']
                elif step == 10:
                    vat_sum += row['amount_multiplied']
                elif step == 15:
                    changes['total'] = row['amount_multiplied']
            changes['vat_total'] = vat_sum
        order.update(changes)
        # Die Formatierung durch die Datenbank klappt noch nicht:
        mf_kwargs = dict(MF_KWARGS[order['la']])
        currency_kwargs = dict(mf_kwargs)
        currency_kwargs['curr'] = normal_currency(order['currency'])
        percent_kwargs = dict(mf_kwargs)
        percent_kwargs.update({
            'places': None,
            'curr': u'%',
            })
        for row in articles:
            row['amount_formatted'] = format_decimal(row['amount'],
                                                     **currency_kwargs)
            row['amount_multiplied_formatted'] = format_decimal(row['amount_multiplied'],
                                                                **currency_kwargs)
        for row in calculated:
            row['amount_formatted'
                ] = row['amount_multiplied_formatted'
                        ] = format_decimal(row['amount_multiplied'], **currency_kwargs)
            if row['step'] == 10:
                row['article_title'] = make_translator(context)(
                        '${percentage} VAT',
                        mapping={'percentage': format_decimal(row['vat_percent'],
                                                              **percent_kwargs),
                                 })
#... (hier evtl. noch Feintuning der MwSt-Angaben)

        hashed = make_secret(order_id)
        order['formid'] = hashed

        for item in articles:  # result['art']
            if item['start']:
                item['start'] = item['start'].strftime(DD_MM_YYYY)

        return result
        # ---------------- ] ... _get_order_articles_and_calculation ]

    @log_or_trace(**lot_kwargs)
    def _get_orders(self, sql,
                    oid=None, payment_status=None,
                    sessionID=None, userID=None):
        """
        Gib stets eine Liste zurück (kein None, und keinen Generator)

        Die alte Logik - ggf. Rückgabe von None, je nach Suchargumenten -
        wurde durch die Unterscheidung der vorliegenden neuen Methode
        _get_orders von der (diese aufrufenden) _get_order abgelöst.

        oid = unitracc_orders.order_id (eine Zahl)
        payment_status  -- textuelle Angabe 'new', 'accepted' etc.

        Sortierung und die Abfrage nach einem nicht-numerischen Zahlungsstatus
        werden erledigt durch die SQL-Sicht "orders_view"

        Für Management-Seiten:
        Es werden keine Benutzer-IDs aus dem Kontext ermittelt oder Buchungen
        neu angelegt
        """
        query_data = {}
        if oid:
            query_data.update({
                'order_id': oid,
                })
        if payment_status:  # z. B. 'new' oder 'accepted'
            query_data.update({
                'payment_status': payment_status,
                })
            # (erübrigt die Abfrage nach booking_states_id)
        if sessionID:
            query_data.update({
                'sessionid': sessionID,
                })
        if userID:  # z. B. 'new' oder 'accepted'
            query_data.update({
                'userid': userID,
                })
            # (erübrigt die Abfrage nach booking_states_id)
        rows = list(sql.select('orders_view',
                               query_data=query_data))
        return rows
        # (alten Code in Rev. 20947 entfernt)

    def _get_order(self, sql, *args, **kwargs):
        """
        Rufe _get_orders auf; erwarte aber nur einen Datensatz und gib
        entsprechend genau einen Datensatz oder None zurück
        """
        res = self._get_orders(sql, *args, **kwargs)
        if res:
            if res[1:]:
                logger.warning('_get_order: Zuviele Datensätze für %(args)s,'
                               ' %(kwargs)s!',
                               locals())
            return res[0]
        return None

    '''
    @log_or_trace(**lot_kwargs)
    def _get_articles(self, sql, order_id, article_id=None):
        """
        Hole alle Artikel die zu einer Bestellung gehören.
        """
        query_data = {'order_id': order_id,
                      }
        if article_id is not None:
            query_data['article_id'] = article_id
        rows = sql.select("orders_articles_view",
                          query_data=query_data)

        return rows
    '''

    @log_or_trace(**lot_kwargs)
    def get_last_ordernumber(self, sql):
        """
        Gib die letzte Ordernumber zurück

        Hilfsmethode für _generate_ordernumber
        """
        for row in sql.query('SELECT max(ordernr) as ordernr'
                             ' FROM unitracc_orders;'):
            return row['ordernr']

    @log_or_trace(**lot_kwargs)
    def get_payment_types(self, type=None, tid=None):
        """
        Zuweisung in ...
        - templates/order_edit.pt
        - templates/order_add.pt

        Holt die Zahlungsarten (msgid: "Payment method") heraus.

        Feld "active":
        0 = inaktiv
        1 = überall aktiv
        2 = nur im backend

        tid  -- numerische ID des Zahlungstyps
                (um den textuellen Namen dieses einen zu ermitteln)
        type -- textueller Name des Zahlungstyps
                (um die ID dieses einen zu ermitteln)
        """
        # TODO: Argument für Frontend/Backend/alle
        with self.sql as sql:
            return self._get_payment_types(sql, type)

    def _get_payment_types(self, sql, payment_type=None):
        # TODO: für interne Verwendung ersetzen durch neuen JOIN
        if payment_type:
            query_data = {'payment_type': payment_type}
        else:
            query_data = {}
        rows = list(sql.select('payment_types_view',
                               query_data=query_data))
        return rows

    @log_or_trace(**lot_kwargs)
    def check_paypal_setup(self):
        """
        Prüfe, ob das PayPal-Setup komplett ist, und gib im Erfolgsfall
        True zurück
        """
        sp = self.context.getBrowser('subportal')
        spdict = sp.get_current_info()
        return bool(spdict.get('paypal_url')
                    and spdict.get('paypal_id'))

    @log_or_trace(**lot_kwargs)
    def get_active_payment_types(self, backend=False, ids_only=False, order_id=None):
        """
        Gib die aktiven Zahlungsarten zurück

        backend -- 0 oder False für Frontend, 1 oder True für Backend
        ids_only -- wenn true, wird nur eine Liste der (numerischen) IDs
                    zurückgegeben

        Wenn "paypal" unter den Zahlungsarten ist, wird die
        Konfiguration geprüft.

        Verwendet in (gf) templates/order_choose_payment_method.pt
        """
        with self.sql as sql:
            return self._get_active_payment_types(sql, backend, ids_only, order_id)

    def _get_active_payment_types(self, sql,
                                  backend=False, ids_only=False, order_id=None):
        # PayPal muß konfiguriert sein; daher jedenfalls payment_type
        # mit ermitteln:
        rows = sql.select('payment_types_view',
                          query_data={'active': ACTIVE_VALUES[backend],
                                      })
        raw = []
        for row in rows:
            if row['payment_type'] == 'paypal':
                if order_id is not None:
                    order_rows = sql.select('unitracc_orders',
                                            fields=['paypal_allowed'],
                                            query_data={'order_id': order_id})
                    if not order_rows:
                        logger.error('get_active_payment_types: order %(order_id)r not found',
                                     locals())
                        raw = []  # Falsche Bestellung, keine Zahlungsarten!
                        break
                    if not order_rows[0]['paypal_allowed']:
                        continue
                if self.check_paypal_setup():
                    pass
                elif ids_only:
                    continue
                else:
                    row['disabled'] = 'setup incomplete'
            raw.append(row)
        if ids_only:
            return [dic['payment_type']
                    for dic in raw]
        else:
            return raw

    @log_or_trace(**lot_kwargs)
    def get_bookable_courses(self):
        """
        Filtere die vorhandenen Kurse danach, ob sie auch wirklich
        buchbar sind, d.h. einen Preis und eine Dauer haben.

        Nota bene: Das trifft für kostenlose Demokurse nicht zu.
        """
        context = self.context
        unitracccourse = context.getBrowser('unitracccourse')
        rc = getToolByName(context, 'reference_catalog')
        res = []
        for brain in unitracccourse.search():
            uid = brain.UID
            try:
                course_obj = rc.lookupObject(uid)
                price = extract_float(course_obj.getPrice_shop())
                float(course_obj.getShopduration())
            except Exception as e:
                print('*' * 79)
                print('E Kursobjekt %(uid)s: %(e)s' % locals())
            else:
                res.append(brain)
        return res

    @log_or_trace(**lot_kwargs)
    def get_booking_status_choices(self, sql=None):
        """
        früher: get_booking_status;
        Abfrage nach numerischer ID ist aber überholt

        Es kommen alle Zeilen der Tabelle zurück,
        - sortiert nach der "id",
        - aber ohne diese (da nun direkt booking_state zu verwenden)

        (derzeit 7 Zeilen)
        """
        if sql is not None:
            return list(sql.select('booking_states_view'))
        with self.sql as sql:
            return list(sql.select('booking_states_view'))

    @log_or_trace(**lot_kwargs)
    def get_article_group(self, uid):
        """
        Hol die Gruppe für den artikel
        (OBSOLET)
        """
        groups = self.context.getBrowser('groups')

        # @TODO: Optimieren für andere Objekte
        group = groups.getById(learner_group_id(uid))
        return group

    @log_or_trace(**updated(lot_kwargs, trace=0))
    def get_order(self, sql=None, **kwargs):  # ------ [ get_order() ... [
        """
        Gib den für die aktuelle Session existierenden Bestellungs-Datensatz zurück;
        dieser wird ggf. zuvor erzeugt.
        """
        pm = getToolByName(self.context, 'portal_membership')
        if pm.isAnonymousUser():
            raise Unauthorized
        if sql is not None:
            return self._get_or_create_order(sql, **kwargs)
        with self.sql as sql:
            return self._get_or_create_order(sql, **kwargs)

    def _get_or_create_order(self, sql, **kwargs):
        context = self.context
        if not kwargs:
            request = context.REQUEST
            kwargs = dict(request.form)

        order_id = kwargs.pop('order_id', None)
        if order_id:  # Buchungs-ID angegeben:
            order = self._get_order(sql, oid=order_id)
            if order:
                return order  # der Datensatz, ein Dict

        user_id = kwargs.pop('user_id', None)
        if not user_id:
            user_id, session_id = self._get_user_and_session(context=context)
            order = self._get_order(sql, payment_status='new',
                                    sessionID=session_id,
                                    userID=user_id)
            if order:
                return order  # der Datensatz, ein Dict

        # noch keine Bestellung; erzeugen:
        data = {
            'date_booked':       date.today(),
            'userid':            user_id,
            'sessionid':         session_id,
        # Checkme: Vorbelegung sinnvoll/notwendig? (vielleicht besser NULL / None)
        # (leider derzeit mit NOT-NULL-Constraint abgesichert; größere Änderung)
            # die Spalte ist NOT NULL; ersetzen durch Standardwert:
            'payment_type':   'prepayment',
            # die Spalte ist NOT NULL; ersetzen durch Standardwert:
            'booking_state':  'new',
            # in diesem Stadium noch nicht benötigt:
            # 'ordernr':           self._generate_ordernumber(sql),
            'la':                getActiveLanguage(context),
            }
        return self._insert_order(sql, data)  # ------ ] ... get_order() ]

    @log_or_trace(trace=0, **lot_kwargs)
    def add_article(self):  # ------------------- [ add_article ... [
        """
        Füge den Artikel <uid> (aus Formulardaten) der Bestellung hinzu;
        die gegebenenfalls noch nicht vorhandene Bestellung wird erzeugt durch
        den Aufruf von --> get_order (impliziert --> _insert_order).
        Anschließend Umleitung zur Ansicht der Bestellung.

        Diese Methode wird vom "klassischen" Unitracc-Buchungssystem verwendet
        und dient der einfachen Kursbuchung per AJAX-Request.

        Derzeit muß man angemeldet sein, um etwas bestellen zu können.
        """
        context = self.context
        getBrowser = context.getBrowser
        pm = getToolByName(context, 'portal_membership')
        if pm.isAnonymousUser():
            raise Unauthorized

        portal = getToolByName(context, 'portal_url').getPortalObject()
        desktop_path = context.getBrowser('unitraccfeature').desktop_path()
        rc = getToolByName(context, 'reference_catalog')
        request = context.REQUEST
        is_post_request = request.get('REQUEST_METHOD') == 'POST'

        form = request.form
        article_uid = form.get('uid', None)
        if not article_uid:
            return

        with self.sql as sql:
            # Bestellung ermitteln, ggf. vorher anlegen:
            order = self.get_order(sql, **dict(form))

            hub, info = make_hubs(self.context)
            is_post = info['request_var'].get('post')
            try:
                self._add_article(sql, hub, info, article_uid, order)
            except Redirect as e:
                logger.exception(e)
                logger.info('add_article: %(e)r', locals())
                if is_post:
                    return "false"
                raise
            # Post Request via JS ?
            url = portal.absolute_url() + desktop_path + '/mycart'
            if is_post:
                return url
            else:
                return request.RESPONSE.redirect(url)
    # ------------------------------------------- ] ... add_article ]

    def update_order(self, hub=None, info=None): # --------- [ update_order ... [
        """
        Aktualisiere den Einkaufswagen aus Formulardaten

        Es wird zunächst die aktuelle Auswahl aus der Datenbank gelesen und ggf. erzeugt;
        aus den Formulardaten werden UIDs und etwaige zugeordnete Anzahl ausgelesen.

        Schon vorhandene Artikel im Einkaufswagen werden aktualisiert oder (mit quantity=0)
        gelöscht; neue werden eingefügt.

        Bei den meisten Datensätzen wird quantity = None sein; diese werden übergangen.
        Ausnahme ist die UID aus "button_uid": Wenn diese noch nicht im Einkaufswagen liegt,
        wird ggf. die Anzahl 1 ergänzt.

        Aufgerufen aus visaplan.UnitraccShop.
        """
        if hub is None:
            hub, info = make_hubs(self.context)
        with self.sql as sql:
            form = info['request_var']
            # wenn ein Bestellbutton neben einem leeren Zahlenfeld angeklickt wurde,
            # wird als Anzahl 1 angenommen (visaplan.UnitraccShop@21475):
            uid_from_button = form.pop('button_uid', None)
            # Auftrag nötigenfalls erzeugen:
            order = self.get_order(sql)
            query_data = subdict_forquery(order, ['order_id'])
            order_id = query_data['order_id']

            # wg. Zugriffs auf diverse Felder (q&d):
            sm = info['portal_object'].getAdapter('securitymanager')
            sm(userId='system')
            sm.setNew()
            try:
                # was liegt schon im Einkaufswagen?
                articles = list(sql.select('articles_items_view',
                                           query_data=query_data))
                quantity_in_cart, uids_in_cart = in_cart(articles)

                form_uids = []
                invalid_input_found = False
                insert_list = []
                deleted_uids = set()
                deletions, changes = 0, 0
                # --------------- [ iteriere über Formulardaten ... [
                for dic in sorted(list(form.values()), key=attrgetter('number')):
                    dic = dict(dic)
                    uid = dic['article_uid'] = dic.pop('uid')
                    quantity = dic.get('quantity')
                    if (quantity is None
                        and uid == uid_from_button
                        and uid not in uids_in_cart
                        ):
                        quantity = 1
                    # leere Eingabefelder werden ansonsten ignoriert:
                    if quantity is None or uid is None:
                        continue
                    if not isinstance(quantity, int):
                        try:
                            quantity = int(quantity)
                        except ValueError:
                            invalid_input_found = True
                            hub['message']('Skipped non-number value "${quantity}"',
                                           'error',
                                           mapping=locals())
                            logger.error('non-integer quantity %(quantity)r in %(dic)s',
                                         locals())
                            continue
                        else:
                            if quantity < 0:
                                invalid_input_found = True
                                hub['message']('Negative quantities are not allowed!'
                                               ' (${quantity})'
                                               'error',
                                               mapping=locals())
                                continue
                            dic['quantity'] = quantity
                    if 'number' in dic:  # Sortierungsfeld
                        del dic['number']
                    # ------------ [ zunächst UPDATE und DELETE ... [
                    if uid in uids_in_cart:
                        if (quantity == quantity_in_cart[uid]
                            and quantity
                            ):
                            # unveränderte Anzahl gr. 0 --> nichts tun
                            continue
                        article_qd = {'order_id': order_id,
                                      'article_uid': uid,
                                      }
                        if quantity:
                            rows = list(
                                sql.update('unitracc_orders_articles',
                                           {'quantity': quantity,
                                            },
                                           query_data=article_qd,
                                           returning='*'))
                            affected = len(rows)
                        else:
                            rows = list(
                                sql.delete('unitracc_orders_articles',
                                           query_data=article_qd,
                                           returning='*'))
                            affected = len(rows)
                            deletions += affected
                            deleted_uids.add(uid)
                        changes += affected
                        if affected != 1:
                            partizip = quantity and 'updated' or 'deleted'
                            logger.error('%(affected)d rows %(partizip)s (1 expected); '
                                         'query_data=%(article_qd)s',
                                         locals())
                    # ------------ ] ... zunächst UPDATE und DELETE ]
                    elif quantity:  # noch nicht im Einkaufswagen:
                        insert_list.append((uid, quantity))
                # --------------- ] ... iteriere über Formulardaten ]
                # Abgeleitete Auftragsdaten zurücksetzen:
                update_so_far = {
                    'currency': None,
                    'paypal_id': None,
                    'paypal_allowed': True,
                    }
                order.update(update_so_far)
                try:
                    # Bisherige Artikel:
                    for item in articles:
                        uid = item['article_uid']
                        if uid in deleted_uids:
                            continue
                        # ergibt bei Unverträglichkeit eine gute Fehlermeldung:
                        article, update = article_dicts(uid, order, hub, info)
                        # ohne Befund; aktualisieren:
                        order.update(update)
                        # der Auszug für das SQL-Update:
                        update_so_far.update(update)
                    # ... dann INSERT:
                    if insert_list:
                        # Es wird eingefügt - Verträglichkeit muß geprüft werden!
                        # Jetzt die neuen:
                        for (uid, quantity) in insert_list:
                            article, update = article_dicts(uid, order, hub, info,
                                                            quantity)
                            # OK; einfügen:
                            sql.insert('unitracc_orders_articles',
                                       article)
                            changes += 1
                            order.update(update)
                            # der Auszug für das SQL-Update:
                            update_so_far.update(update)
                    if changes:
                        # Hier wird die *Bestellung* geändert (1254: nach der akt. Zeilennummer)
                        assert 'article_uid' not in query_data, (
                                'assertion 1254: %(query_data)r'
                                ) % locals()
                        update4order = subdict_forquery(update_so_far, keys=None, strict=False)
                        # ist derzeit stets gefüllt, wg. Vorbelegung paypal_allowed=True:
                        if update4order:
                            sql.update('unitracc_orders',
                                       update4order,
                                       query_data=query_data)
                except UnitraccBaseException as e:
                    hub['message'](**e.message_kwargs())
            finally:
                sm.setOld()
            # ---------------------------------- ] ... update_order ]

    @log_or_trace(trace=0, **lot_kwargs)
    def _add_article(self,  # ------------------ [ _add_article ... [
                     sql,
                     hub, info, article_uid, order, quantity=1,
                     vat_percent=None,
                     discount_group='course',
                     certificate_text=None,
                     certificate_price=None):
        """
        Arbeitspferd für --> add_article;
        außerdem direkt aufgerufen durch visaplan.UnitraccShop.

        Neue Optionen:
        quantity -- kann nun Werte ungleich 1 annehmen und muß bei der
                    Berechnung berücksichtigt werden
        discount_group --
                    Bestellposten derselben Rabattgruppe werden für die
                    Berechnung der Rabattstufe zusammengefaßt (drei Buchungen
                    desselben Kurses werden genauso behandelt wie drei
                    Einzelbuchungen unterschiedlicher Kurse)
        certificate_text --
                    Auszugebender Beschreibungstext,
                    z. B. "incl. Abschlußtest und Zertifikat"
        certificate_price --
                    Preis des Zertifikats, der zum Preis des Kurses
                    hinzugerechnet wird.
                    (ein vom Kurs abweichender Mehrwertsteuersatz für das Zertifikat
                    wird noch nicht unterstützt)
        """
        if not isinstance(order, dict):
            pp(order=order)
            logger.error('Hu? %(order)r ist kein Dict', locals())
            # set_trace()
        order_id = order['order_id']
        # Hier noch kein Vorgabewert - er könnte mit der Festlegung durch einen
        # Artikel kollidieren:
        order_currency = order.get('currency')
        order_paypal_id = order.get('paypal_id')

        is_post = info['request_var'].get('post')

        sm = info['portal_object'].getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()

        try:
            try:
                article, order_update = article_dicts(article_uid, order,
                                                      hub, info,
                                                      quantity)
            except BookingConfigurationError as e:
                if not info['request_var'].get('post'):
                    kwargs = e.message_kwargs()
                    if not info['has_perm']['Manage portal']:
                        kwargs['message'] = ('Sorry, can\'t add ${title}; '
                                'a configuration error occurred.')
                    hub['message'](**kwargs)
                return back_to_referer(info['context'])
            except UnitraccBaseException as e:
                if not info['request_var'].get('post'):
                    hub['message'](**e.message_kwargs())
                return back_to_referer(info['context'])
            else:
                if order_update:
                    sql.update('unitracc_orders',
                               order_update,
                               query_data={'order_id': order_id})
                return sql.insert('unitracc_orders_articles', article)
        except IntegrityError as e:
            if article:
                hub['message']('"${article_title}" is already present '
                               'in your shopping cart.',
                               'error',
                               mapping=article)
            else:
                hub['message']("Sorry, this didn't work. Perhaps some item"
                               ' was already present in your shopping cart?',
                               'error')
            return back_to_referer(info['context'])
        finally:
            sm.setOld()
    # ------------------------------------------ ] ... _add_article ]

    @log_or_trace(**lot_kwargs)
    def insert_backend_booking(self):  # - [ i._backend_booking ... [
        """
        Annehmen der Formulardaten einer Buchung
        und Prozessierung der Speicherung

        Aufgerufen aus (gf) templates/order_add.pt.
        """

        context = self.context
        checkperm = getToolByName(context, 'portal_membership').checkPermission
        if not checkperm('Manage Orders', context):
            raise Unauthorized
        request = context.REQUEST
        form = request.form
        portal = getToolByName(context, 'portal_url').getPortalObject()
        redirect = request.RESPONSE.redirect
        if form.get('cancel'):
            return redirect(portal.absolute_url() + '/order_management')
        rc = getToolByName(context, 'reference_catalog')
        supported_fields = REQUIRED_FIELDS + [
                'user',  # Fallback für userid
                ]
        retry_url = tryagain_url(request, list(form.keys()))

        # ------------------------ ] ... insert_backend_booking ... [
        # TH: ist das nötig?
        sm = context.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()
        hub, info = make_hubs(context)
        # zumindest try/finally; ContextManager?
        try:
            required_filled = True
            order = form
            if not form.get('userid', None):
                order['userid'] = form.get('user', '')

            for item in REQUIRED_FIELDS:
                if not order.get(item, None):
                    required_filled = False
                    break

            if not required_filled:
                message(context, 'Please fill all required fields',
                        'error')
                return redirect(retry_url)

            if (not form.get('lastname', None) and not form.get('company', None)):
                message(context, 'Please fill first and lastname or company',
                        'error')
                return redirect(retry_url)

            # -------------------- ] ... insert_backend_booking ... [
            user = context.getBrowser('author').getByUserId(order['userid'])
            if not user:
                message(context, 'Please use a valid user',
                        'error')
                return redirect(retry_url)
            # prepare article
            # Vorerst nur ein Artikel aus dem Backend zum Testen
            article_uid = form.get('article', None)
            # -------------------- ] ... insert_backend_booking ... [
            # Order Objekt einfügen und Speichern.
            with self.sql as sql:
                order = form
                order.pop("article", None)
                order.pop("start", None)
                quantity = int(order.pop('quantity', '1'))
                try:
                    order['booking_state'] = 'paying'
                    order['ordernr'] = self._generate_ordernumber(sql)
                    order = self._insert_order(sql, order)
                    order_id = order['order_id']
                    try:
                        article, order_update = article_dicts(article_uid, order,
                                                              hub, info,
                                                              quantity)

                    except UnitraccBaseException as e:
                        if not info['request_var'].get('post'):
                            message(context, e.message_kwargs())
                        return back_to_referer(request=request)
                    else:
                        if order_update:
                            sql.update('unitracc_orders',
                                       order_update,
                                       query_data={'order_id': order_id})
                        sql.insert('unitracc_orders_articles', article)
                except IntegrityError as e:
                    message(context,
                            'This object is already present in your '
                            'shopping cart.',
                            'info')
                    return back_to_referer(request=request)

                orderdata = self._get_order_articles_and_calculation(sql, order=order)

            # self._send_confirmation_mails(order, articles, user)
            # templates/mail_order_confirmation.pt
            self._send_mail('mail_order_confirmation',
                            hub, info,
                            orderdata=orderdata,
                            subject_type='thankyou')
            # templates/mail_order_new.pt
            self._send_mail('mail_order_new',
                            hub, info,
                            orderdata=orderdata,
                            to_admin=True,
                            subject_type='thankyou')

            message(context, "Entry saved")
            if form.get('post'):
                return "Ok"
            return redirect(portal.absolute_url() + '/order_management')
        finally:
            sm.setOld()
            # ------------------------ ] ... insert_backend_booking ]

    @log_or_trace(**lot_kwargs)
    def _send_confirmation_mails(self, order, articles, user):
        """
        Sende Auftragsbestätigungsmail an den Kunden
        und nachrichtliche Mail an das Buchungsteam

        Mails an orders/booking@unitracc.de & Kunden
        order = Dict der Buchung
        articles = Liste der gebuchten Artikel
        user = Author object
        """
        # TODO: Komplette Information über etwaige Rabatte entgegennehmen und verwenden
        context = self.context
        portal = getToolByName(context, 'portal_url').getPortalObject()

        options = {'order': order,
                   'articles': articles,
                   'greeting': self.make_greeting(order),
                   'domain': portal.absolute_url(),
                   }

        hub, info = make_hubs(self.context)
        config = self._get_subportal_config(hub, info)
        mail_from = self.get_sending_mail_address(hub, info)

        # Send User mail; templates/mail_order_confirmation.pt
        _template_user = "mail_order_confirmation"
        # --> ._send_mail(subject_type='thankyou')
        subject = self._order_mail_subject(hub, info, order, config,
                                           type='thankyou')
        mail = context.getBrowser('unitraccmail')
        mail.set('utf-8', _template_user, subject, options)
        mail.renderAsHTML()
        user_email = user.getEmail()
        if debug_active:
            pp((('Mail-Template (User):', _template_user),
                ('options-dict fuer Mail:', options),
                ('user:', user),
                ('mail.email:', mail.email),
                ))
        # --> ._send_mail(to_admin=False) (Vorgabe)
        message = getMessenger(context)
        sendMail(mail, mail_from, user_email, message,
                 subject=subject)

        # Send unitracc team mail
        # die folgende Mail-Adresse ist hier falsch:
        # mail_to = env.get('editorial', 'info@unitracc.de')
        # templates/mail_order_new.pt
        _template_editorial = "mail_order_new"
        subject = self._order_mail_subject__backend(hub, info, order, config)
        options.update({'user_email': user_email,
                        'userid': order['userid'],
                        })
        mail.set('utf-8', _template_editorial, subject, options)
        mail.renderAsHTML()
        if debug_active:
            pp((('Mail-Template (Admin):', _template_editorial),
                ('options-dict fuer Mail:', options),
                ('user:', user),
                ('mail.email:', mail.email),
                ))
        # für diese Mail nur Logging, keine Flash-Message:
        sendMail(mail, mail_from, mail_from,
                 subject=subject)

    @log_or_trace(**lot_kwargs)
    def _insert_order(self, sql, data):
        """
        Einfügen einer Buchung in die Datenbank

        Neu seit 2/2018:
        Gibt nicht mehr nur die ID, sondern den neu eingefügten Datensatz zurück
        """
        request = self.context.REQUEST
        table = "unitracc_orders"

        data.pop('user', None)
        data['date_booked'] = datetime.today()
        data['ip'] = request.get('HTTP_X_FORWARDED_FOR', "0.0.0.0")
        data['sessionid'] = request['SESSION'].getId()
        # 'returning' erzeugt einen Generator:
        for row in sql.insert(table, data, returning='*'):
            return row

    @log_or_trace(**lot_kwargs)
    def update_order_payment(self):
        """
        Zum Aufruf aus dem Backend (cart.js, JS-Funktion acceptpayment):

        Aktualisiert den Zahlungsstatus
        und erteilt ggf. Zugriff auf die gebuchten Objekte
        """
        form = self.context.REQUEST.form
        userBrowser = self.context.getBrowser('author')
        user = userBrowser.getByUserId(order['userid'])
        order_id = form.get('set', None)
        status = form.get('status', 'accepted')
        try:
            # kurzfristig: Formular mit alter Version abgeschickt,
            # enthält noch eine Zahl:
            status_id = int(status)
            status = OLD2NEW_STATUS[status_id]
        except ValueError:
            pass  # prima, schon ein String
        except KeyError:
            logger.error('update_order_payment: unknown status value %(status_id)r',
                         locals())
        with self.sql as sql:
            self._update_order_payment(sql, user, status, order_id, backend=True)
        return "ok"

    @log_or_trace(**lot_kwargs)
    def _update_order_payment(self, sql, user, status, order_id, backend=False):
        """
        Aktualisiert den Zahlungsstatus
        und erteilt ggf. Zugriff auf die gebuchten Objekte.
        Das Zahlungsdatum ist immer <heute>.
        Arbeitspferd für die Methode update_order_payment.

        user -- ein Benutzerprofil wie vom author-Browser zurückgegeben
        status -- numerischer Zahlungsstatus
        order_id -- unitracc_orders.order_id (PK; eine Zahl) <--> item_number
        backend -- True, wenn die Aktion durch das Backend ausgelöst wurde
        """
        assert isinstance(status, six_string_types), (
            'status: String erwartet (%(status)r)'
            ) % locals()
        update = {'booking_state': status,
                  }
        access_granted = status in ('accepted',)
        if access_granted:
            update['date_payed'] = datetime.today()
        sql.update('unitracc_orders', update,
                   query_data={'order_id': order_id})
        # ggf. Zugriff erteilen und Mails senden:
        self._order_access_and_mails(sql, user, status, order_id, backend)

    @log_or_trace(**lot_kwargs)
    def _order_access_and_mails(self, sql, user, status, order_id, backend):
        """
        Erteile Zugriff (wenn status == 'accepted'),
        und sende Mails:
        - an den Nutzer, wenn (bisher) 'accepted' oder 'pending';
        - an die Backend-Mail-Adresse, wenn (not backend)

        user -- ein Benutzerprofil wie vom author-Browser zurückgegeben
        status -- numerischer Zahlungsstatus
        order_id -- unitracc_orders.order_id (PK; eine Zahl) <--> item_number
        backend -- True, wenn die Aktion durch das Backend ausgelöst wurde
        """
        assert isinstance(status, six_string_types), (
            'status: String erwartet (%(status)r)'
            ) % locals()
        access_granted = status in ('accepted',)
        # TODO: SQL-Sicht für JOIN von Buchung und Artikeln
        order = self._get_order(sql, oid=order_id)
        articles = list(sql.select('orders_articles_view',
                                   query_data={'order_id': order_id,
                                               }))
        if backend or not access_granted:
            payment_info = self._get_payment_details(sql, order_id)
        if access_granted:
            for article in articles:
                self._manage_access(sql, article, order['userid'], order_id)

            if 0:  # abzulösende Methode:
                self._send_success_mail(user, order, articles)
            self._send_mail('mail_order_success',
                            hub, info,
                            orderdata=orderdata,
                            # start = start_ddmmyyyy für alle Artikel
                            # duration entsprechend
                            )

        elif status in ('pending',):
            if 0:  # abzulösende Methode:
                self._send_pending_mail(user, order, articles, payment_info)
            self._send_mail('mail_payment_pending',
                            hub, info,
                            orderdata=orderdata,
                            payment_info=payment_info)
        else:
            # TODO: Mails an User in anderen Fällen?
            pass
        if not backend:
            if 0:  # abzulösende Methode:
                self._send_backend_mail(user, order, articles, payment_info)
            self._send_mail('mail_payment_backend',
                            hub, info,
                            orderdata=orderdata,
                            to_admin=True)
        elif 1:
            pass
        elif debug_active:
            DEBUG('debug_active -> _send_backend_mail(...)')
            self._send_backend_mail(user, order, articles, payment_info)

    # @log_or_trace(**lot_kwargs)
    def _get_payment_details(self, sql, order_id):
        # FIXME: SQL, --> dbcursor
        for row in sql.select(
                'latest_paypal_record_view',
                query_data={'unitracc_orders_id': order_id,
                            },
                maxrows=1):
            return row
        return {}

    # @log_or_trace(**lot_kwargs)
    def update_payment(self, status, order_id):
        """
        Aktualisieren des Payment Status
        """
        assert isinstance(status, six_string_types), (
            'status: String erwartet (%(status)r)'
            ) % locals()
        # TH, nachsehen: wo aufgerufen?
        # (siehe auch update_order_payment)
        with self.sql as sql:
            sql.update("unitracc_orders",
                       {'booking_state': status,
                        'date_booked':   datetime.today(),
                        },
                       query_data={'order_id': order_id})
        return "ok"

    @log_or_trace(**lot_kwargs)
    def edit_order(self):
        """
        Verwendung: Formularaktion in templates/order_edit.pt
        Verarbeiten der Daten.
        """
        context = self.context
        request = context.REQUEST
        form = request.form
        redirect = request.RESPONSE.redirect

        view_url = tryagain_url(request, ['id'], path="order_view")
        query_data = subdict(form,
                             ['order_id'],
                             primary_fallback='id',
                             do_pop=True)
        order_id = query_data['order_id']
        if form.get('cancel'):
            return redirect(view_url)
        ok = True
        status = None

        with self.sql as sql:
            # Zahlungsinformation
            status = form.get('booking_state')
            if status:
                date_paid = form.get('date_payed')
                order = self._get_order(sql, oid=order_id)
                # Neuer Status als bezahlt keine Bestellnummer vorhanden.
                if status:
                    if (not order['ordernr']
                        and status in ['pending', 'accepted',
                                       'declined', 'timeout']
                        ):
                        form['ordernr'] = self._generate_ordernumber(sql)

                    # Datums Prüfung
                    if not date_paid and status in ACCEPTED_OR_BETTER:
                        date_paid = datetime.today()

                    if not date_paid:
                        form['date_payed'] = None
                    elif isinstance(date_paid, DateTime):  # von :date
                        formatted = date_paid.ISO8601()
                        form['date_payed'] = formatted
                    elif not isinstance(date_paid, six_string_types):
                        form['date_payed'] = date_paid
                    else:
                        raw = form['date_payed']
                        try:
                            form['date_payed'] = datetime.strptime(raw, DD_MM_YYYY)
                        except ValueError:
                            message(context,
                                    "Unsupported date format (${raw})",
                                    'error',
                                    mapping=locals())
                            ok = False

            if not ok:
                form['id'] = order_id
                retry_url = tryagain_url(request,
                                         ['id', 'booking_state',
                                          ])
                return redirect(retry_url)

            sql.update('unitracc_orders', form,
                       query_data=query_data)

            # Achtung - sucht im portal_user_catalog:
            userBrowser = context.getBrowser('author')
            user = userBrowser.getByUserId(order['userid'])
            # ggf. Zugriff erteilen und Mails senden:
            self._order_access_and_mails(sql, user, status, order_id, backend=True)

            message(context,
                    "Changes saved.")
            return redirect(view_url)

    # @log_or_trace(**lot_kwargs)
    def edit_article(self):
        """
        Aktualisieren der Artikel zu einer Bestellung aus dem Backend
        (templates/order_edit.pt)
        """
        context = self.context
        request = context.REQUEST
        form = request.form

        rc = getToolByName(context, 'reference_catalog')

        oid = form.pop('id')
        if form.get('cancel'):
            return request.RESPONSE.redirect(
                                                "/order_view?id=%s" % oid)
        articles = {}
        articlesold = {}
        with self.sql as sql:
            data = self._get_order_articles_and_calculation(sql, order_id=oid)
            # noch nicht scharf;
            # erst den nachfolgenden Verhau vollständig durchdringen:
            #for article_row in data['articles']:
            #    article_uid = row['article_uid']
            #    articlesold[article_uid] = row
            pp(data=('noch nicht verwendet ...',
                     data,
                     '... noch nicht verwendet'),
               form=dict(form))
            # set_trace()
            for key, value in form.items():
                id, field = key.split("-")
                if articles.get(id):
                    # nur schreiben wenn nicht schon belegt (z.b. durch neuen Kurs)
                    if not articles[id].get(field):
                        articles[id][field] = value

                else:
                    articles[id] = {field: value}
                    articlesold[id] = sql.select('orders_articles_view',
                                                 query_data={'order_id': oid,
                                                             'article_id': id,
                                                             })[0]

                # nur überschreiben, wenn neuer Kurs angegeben
                if (field == "article_uid"
                    and articlesold[id]['article_uid'] != value
                    ):
                    article_object = rc.lookupObject(value)
                    try:
                        price = extract_float(article_object.getPrice_shop())
                        float(article_object.getShopduration())
                    except:
                        # FIXME: Mail-Adresse in Message-ID!
                        message(context, "Booking not possible. Incomplete record."
                                  " Please contact support (info@unitracc.com)."
                                  , 'error')
                        return back_to_referer(request=request)
                    vat = round(price * VAT_PERCENTAGE, 2)
                    articles[id]['article_title'] = article_object. \
                                                    pretty_title_or_id()
                    articles[id]['duration'] = article_object.getShopduration()
                    articles[id]['vat'] = str(vat).replace(".", ",")
                    articles[id]['amount'] = str(price).replace(".", ",")
                if field == "start":
                    if value != "":
                        try:
                            articles[id][field] = datetime.strptime(value,
                                                                    DD_MM_YYYY)
                        except ValueError:
                            message(context, "Wrong date format. "
                                      "The correct input format is: DD.MM.YYYY")
                            return back_to_referer(request=request)
                    else:
                        articles[id][field] = None

            for key in articles.keys():
                articles[key]['order_id'] = oid
                sql.update('unitracc_orders_articles',
                           articles[key],
                           query_data={'article_id': key})
        message(context, "Changes saved.")
        return request.RESPONSE.redirect("/order_view?id=%s" % oid)

    # @log_or_trace(**lot_kwargs)
    def edit_order_view(self, order_id):
        """
        Verwendung in templates/order_edit.pt

        Eine bestehende Bestellung editieren.
        """
        if not order_id:
            return
        with self.sql as sql:
            order = self._get_order(sql, oid=order_id)
            return self._get_order_articles_and_calculation(sql, order)

    # @log_or_trace(**lot_kwargs)
    def get_order_view(self, order_id):
        """
        Ermittle die Daten für die Bestellungsansicht (templates/order_view.pt)
        """
        if not order_id:
            return
        with self.sql as sql:
            order = self._get_order(sql, oid=order_id)
            return self._get_order_articles_and_calculation(sql, order)

    @log_or_trace(**lot_kwargs)
    def _manage_access(self, sql, db_object, user, order_id):
        """
        Erteile dem übergebenen Nutzer Zugriff auf den Artikel.

        db_object -- dict (Daten der Tabellenzeile)
        user -- Benutzerobjekt
        order_id -- numerische Bestellnummer
        """

        def makedate(s):
            """
            Mache Datum aus String
            """
            if s:
                liz = list(map(int, s.split('.')))
                assert len(liz) == 3, '"d.m.yyyy" date value expected (%r)' % s
                liz.reverse()
                return date(*tuple(liz))
            return None
        today = date.today()
        wished_start = db_object['start']
        try:
            group_id = db_object['group_id']
            if group_id is None:
                logger.error('Keine Gruppen-ID im Datensatz %s', (db_object,))
                return  # besserer Rückgabewert?
            groups = self.context.getBrowser('groups')
        except KeyError:
            # Funktionalität aus Methode get_article_group
            logger.warning('Alter Datensatz ohne GruppenID-Feld: %s', (db_object,))
            article_uid = db_object['article_uid']
            group_id = learner_group_id(article_uid)

        if group_id:
            group = groups.getById(group_id)
        else:
            logger.error('Keine Gruppenzuordnung! %s', (db_object,))
            return  # besserer Rückgabewert?

        direct = True
        # Wunschdatum kann nicht eingehalten werden.
        if not wished_start:
            start = today
        else:
            wished_start = makedate(wished_start.strftime(DD_MM_YYYY))
            if today > wished_start:
                start = today
            else:
                start = wished_start
                direct = False
        days = db_object['duration']
        ends = start + timedelta(days=days)
        sql.insert("unitracc_groupmemberships",
                   {'group_id_': group.getId(),
                    'member_id_': user,
                    'start': start,
                    'ends': ends,
                    'order_id': order_id,
                    })
        if direct:
            group.addMember(user)
        return "Ok"

    @log_or_trace(**lot_kwargs)
    def delete_article(self):
        """
        Button-Aktion in ...
        - templates/mycart.pt
        - templates/order_edit.pt
        - templates/booking_macros.pt (Makro "order-overview")

        Einen Artikel aus meiner Bestellung löschen.
        """
        context = self.context
        request = context.REQUEST
        form = request.form
        checkperm = getToolByName(context, 'portal_membership').checkPermission
        # TODO: Konstante verwenden
        # XXX: Berechtigung als Weiche hier problematisch!
        logger.info('delete_article: form=%(form)r', locals())
        try:
            order_id, article_id = form['set'].split('_', 1)
        except KeyError:
            message(context,
                    'No order and/or article ids specified',
                    'error')
            return back_to_referer(request=request)
        except Exception as e:
            logger.error('delete_article: Unexpected error!')
            raise

        if checkperm('unitracc: Manage Orders', context):
            oid = form.get('set')
            go_kwargs = {
                'oid': order_id,
                }
        else:
            oid = form.get('set', '')
            user_id, session_id = self._get_user_and_session(context=context)
            go_kwargs = {
                'payment_status': 'new',
                'sessionID': session_id,
                'userID': user_id,
                }
        if not oid:
            # TODO: bessere Meldung
            message(context,
                    'No properties selected. Unable to delete.',
                    'error')
            return back_to_referer(request=request)

        with self.sql as sql:
            found = False
            # set_trace()
            for order in self._get_orders(sql, **go_kwargs):
                order_id = order['order_id']
                rows = sql.delete('unitracc_orders_articles',
                                  query_data={'article_id': article_id,
                                              'order_id': order_id,
                                              },
                                  returning='article_id')
                found = True
                deleted = len(list(rows))
                if deleted:
                    message(context,
                            'The selected article has been successfully '
                            'removed from the cart.')
                logger.info('delete_article: %(deleted)d articles deleted'
                            ' from order %(order_id)r',
                            locals())
            # TODO: bessere Meldung
            if not order:
                message(context,
                        'No access possible. The operation was interrupted.',
                        'error')
            return back_to_referer(request=request)

    @log_or_trace(**lot_kwargs)
    def _delete_expired_order(self, sql):
        """
        Eine abgelaufene Bestellung komplett aus dem System löschen

        Es werden Bestellungen des aktuell angemeldeten Benutzers gelöscht,
        - wenn die 'sessionid' ungleich der aktuellen Session
          und
        - der Zahlungsstatus 'new' ist
        """
        user_id, session_id = self._get_user_and_session(context=self.context)

        oids = set()
        for order in self._get_orders(sql, payment_status='new',
                                      userID=user_id):
            if order['sessionid'] == session_id:
                continue
            oids.add(order['order_id'])
        if oids:
            self._delete_order(sql, sorted(oids))
        return "Ok"

    # @log_or_trace(**lot_kwargs)
    def delete_order(self, sets=None):
        """
        Verwendung: AJAX-Request aus ../../skins/unitracc_resource/cart.js
        Eine Bestellung aus dem System komplett löschen
        """
        fdata = self.context.REQUEST.form
        sets = fdata.get('set', sets)
        if not sets:
            return
        with self.sql as sql:
            self._delete_order(sql, sets)
        return "Ok"

    def _delete_order(self, sql, sets):
        if not sets:
            return
        # Erst die Gruppenmitgliedschaften löschen
        sql.delete("unitracc_groupmemberships",
                   query_data={'order_id': sets,
                               })
        sql.delete("unitracc_orders_articles",
                   query_data={'order_id': sets,
                               })
        sql.delete("unitracc_orders",
                   query_data={'order_id': sets,
                               })

    @log_or_trace(**lot_kwargs)
    def process_cart(self):
        """
        Formularaktion in templates/mycart.pt:
        ergänzt fehlende Daten für unitracc_orders
        aus dem Benutzerprofil

        Vom Einkaufswagen (Step 1: mycart)
        zur Kasse         (Step 2: checkout)
        """
        hack = self.check_access()
        if hack:
            return hack

        context = self.context
        portal = getToolByName(context, 'portal_url').getPortalObject()
        request = context.REQUEST
        form = request.form
        getBrowser = context.getBrowser
        desktop_path = context.getBrowser('unitraccfeature').desktop_path()
        # set_trace()  # _update_article noch benötigt?
        with self.sql as sql:
            for key, value in form.items():
                if key.startswith('start') and value:
                    a_id = key.split("_")[1]
                    start = datetime.strptime(value, DD_MM_YYYY).date()
                    data = {'start': start}
                    # self._update_article(sql, a_id, data)
                    sql.update('unitracc_orders_articles',
                               data,
                               query_data={'article_id': a_id,
                                           })

            order_id = form.get('oid')
            formid = make_secret(order_id)
            if form.get('formid', '') == formid:
                userid = context.getBrowser('member').getId()
                userbrain = context.getBrowser('author').getBrainByUserId(userid)

                new_data = {}

                for getKey, key in AUTHOR_BRAIN_TO_DB.items():
                    val = userbrain[getKey] or None
                    if val is not None:
                        if key == 'country':
                            countrylist = context.getBrowser('voccountry')
                            val = countrylist.get_country_for_code(val)
                        new_data[key] = val
                if new_data:
                    sql.update('unitracc_orders',
                               dict_of_values=new_data,
                               # nur nach unverändertem Datensatz suchen:
                               where=UNTOUCHED_ORDER_WHERE,
                               query_data={'order_id': order_id,
                                           })
                return request.RESPONSE.redirect(
                                        '%s%s/checkout?formid=%s'
                                        % (portal.absolute_url(),
                                           desktop_path,
                                           formid))

            return request.RESPONSE.redirect(
                                    portal.absolute_url() + desktop_path + '/mycart')

    @log_or_trace(**lot_kwargs)
    def process_order_register(self):
        """
        Rechnungsdaten entgegennehmen und verarbeiten.
        """
        context = self.context
        portal = getToolByName(context, 'portal_url').getPortalObject()
        request = context.REQUEST
        form = request.form
        hack = False
        formid = form.get('formid')
        getBrowser = context.getBrowser
        user_id, session_id = self._get_user_and_session(context=context)
        with self.sql as sql:
            order = self._get_order(sql, payment_status='new',
                                    sessionID=session_id,
                                    userID=user_id)

            #------------------------------#
            # Prüfen ob der Nutzer sich    #
            # auf die Seite "gehackt" hat. #
            #------------------------------#
            hack = self.check_access()
            if hack:
                return hack

            #--------------------------------#
            # Prüfen ob alle Angaben da sind #
            #--------------------------------#
            not_filled = False

            if not form.get('company'):
                if not form.get('firstname') or \
                   not form.get('lastname'):
                    not_filled = True
                    message(context, 'Please enter a name or a company')

            if not form.get('street') or \
               not form.get('zip') or \
               not form.get('city') or \
               not form.get('country'):
                not_filled = True

            if not_filled:
                message(context, 'Please fill all required fields')
                return context.restrictedTraverse('checkout')()

            address_values = dict(form)
            address_values.pop('formid')

            #------------------------#
            # Prozessieren der Daten #
            #------------------------#
            order_id = order['order_id']
            try:
                sql.update('unitracc_orders',
                           address_values,
                           query_data={'order_id': order_id})
            except ProgrammingError as e:
                message(context,
                        'Invalid data!',  # z. B. unbekannte Feldnamen
                        'error')
                # e.pgerror: 'ERROR: ' + e.args[0]
                # e.pgcode: z. B. '42703'
                pgcode = e.pgcode
                pgerror = e.pgerror
                errorclass = e.__class__.__name__
                logger.error('process_order_register: '
                             '%(errorclass)s (pgcode=%(pgcode)r, pgerror=%(pgerror)s)',
                             locals())
                # getestet; die Flash-Message oben wird ausgegeben:
                raise Redirect(back_to_referer(request=request))

            desktop_path = context.getBrowser('unitraccfeature').desktop_path()
            hashed = make_secret(order_id)
            return request.RESPONSE.redirect('%s%s/order_preferences?formid=%s'
                                             % (portal.absolute_url(),
                                                desktop_path,
                                                hashed,
                                                ))

    @log_or_trace(**lot_kwargs)
    def submit_order(self):
        """
        annehmen und Abschicken der Bestellung
        ./templates/order_payment_finished.pt
        """
        context = self.context
        hub, info = make_hubs(context)
        request = context.REQUEST
        form = request.form
        portal = getToolByName(context, 'portal_url').getPortalObject()
        if not form.get('booking_tac'):
            message(context,
                    'Please accept the terms and conditions.',
                    'error')
            redirect = request.RESPONSE.redirect
            return redirect(tryagain_url(request, list(form.keys())))

        #------------------------------#
        # Prüfen ob der Nutzer sich    #
        # auf die Seite "gehackt" hat. #
        #------------------------------#
        hack = self.check_access()
        if hack:
            return hack

        getBrowser = context.getBrowser
        user_id, session_id = self._get_user_and_session(context=context)
        with self.sql as sql:
            order = self._get_order(sql, payment_status='new',
                                    sessionID=session_id,
                                    userID=user_id)
            order_id = order['order_id']

            #-------------------------------#
            # Inhalte für die Mail anpassen #
            #-------------------------------#
            dict_ = self._get_complete_order_info_by_order_id(sql, order_id)
            articles = dict_['articles']
            if not articles:
                # TODO: Meldung, und Umleitung zu guter Zieladresse
                return context.restrictedTraverse('mycart')(order_id=order_id)
            order_update = {
                'booking_state': 'paying',
            }
            if order['ordernr'] is None:
                order_update['ordernr'] = self._generate_ordernumber(sql)
            rows = list(sql.update('unitracc_orders',
                                   order_update,
                                   query_data={'order_id': order_id,
                                               },
                                   returning='*'))
            order.update(rows[0])

            # Mail schicken
            # user = context.getBrowser('author').getByUserId(user_id)
            # TODO: Komplette Information über etwaige Rabatte übergeben
            orderdata = self._get_order_articles_and_calculation(sql, order=order)
            # self._send_confirmation_mails(order, articles, user)
            if 0:
                pp(order)
                set_trace()
            # templates/mail_order_confirmation.pt
            self._send_mail('mail_order_confirmation',
                            hub, info,
                            orderdata=orderdata,
                            subject_type='thankyou')
            # templates/mail_order_new.pt
            self._send_mail('mail_order_new',
                            hub, info,
                            orderdata=orderdata,
                            to_admin=True,
                            subject_type='thankyou')
            # templates/order_payment_finished.pt
            return context.restrictedTraverse('order_payment_finished'
                                              )(
                        order_id=order_id,
                        orderdata=orderdata,
                        user_email=info['user_email'])

    # @log_or_trace(**lot_kwargs)
    def get_complete_order_info_by_order_id(self, order_id):
        """
        Verwendung: Zuweisung in templates/order_payment_finished.pt

        Komplette Daten, u.a. für PayPal-Rückkehrseite:
        Ein dict, mit Schlüsseln:
        'articles' -- Datensatz aus unitracc_orders_articles
        'order' -- Datensatz aus unitracc_orders, mit zusätzlichen Schlüsseln
                   aus _calculate_prices
        """
        with self.sql as sql:
            return self._get_complete_order_info_by_order_id(sql, order_id)

    def _get_complete_order_info_by_order_id(self, sql, order_id):
        # Arbeitspferd für get_complete_order_info_by_order_id
        order = self._get_order(sql, oid=order_id)
        return self._get_order_articles_and_calculation(sql,
                                                        order)

    def get_existing_order(self, hub, info):
        """
        Gib die aktuelle Bestellung zurück, sofern vorhanden;
        ansonsten (und z. B. bei anonymem Zugriff) nur Dummydaten,
        die zur Formatierung von Beträgen ausreichend sind
        """
        result = None
        if info['logged_in']:
            with self.sql as sql:
                order = self._get_current_order(sql)
                if order is not None:
                    result = self._get_order_articles_and_calculation(sql, order=order)
        if result is None:
            result = {
                'order': {
                    'la': info['current_lang'],
                    'order_id': None,  # nur für Testbarkeit
                    },
                'meta': {},
                'articles': [],
                }
        meta = result['meta']
        order = result['order']
        meta['mf_kwargs'] = MF_KWARGS[order['la']]
        return result

    # @log_or_trace(**lot_kwargs)
    def check_access(self, web=False):
        """
        Prüfe den Zugriff

        Erzeugt eine Formularvariable "formid" zur "XSS-Prüfung"
        Die Methode wird durch plone4.csrffixes mutmaßlich obsolet
        (das aber problematisch in der Anwendung ist).
        """
        context = self.context
        desktop_path = context.getBrowser('unitraccfeature').desktop_path()
        portal = getToolByName(context, 'portal_url').getPortalObject()
        _ = make_translator(context)
        request = context.REQUEST
        form = request.form
        user_id, session_id = self._get_user_and_session(context=context)
        with self.sql as sql:
            order = self._get_order(sql, payment_status='new',
                                    sessionID=session_id,
                                    userID=user_id)
        hack = False
        message_ = False
        # Gibt es Bestellungen?
        if not order:
            hack = True
            order_id = '0'
            msg = TIMEOUT_MSGID
            message_ = True
        else:
            order_id = order['order_id']
        # gibt es eine Hashsumme?
        if not form.get('formid'):
            msg = 'No access possible. The operation was interrupted.'
            message_ = True
            hack = True
            logger.error('Order %(order_id)r: hack = %(hack)r', locals())
        formid = form.get('formid')
        hashed = make_secret(order_id)
        # Sind die hashsummen und gleich oder wurde gehackt?
        if formid != hashed or hack:
            logger.error('Order %(order_id)r:\nformid=%(formid)r,\nhashed=%(hashed)r', locals())
            if not message_:
                msg = 'No access possible. The operation was interrupted.'
            if web:
                raise Unauthorized(_(msg))
            message(context, msg, 'error')

            return request.RESPONSE.redirect(
                                portal.absolute_url() + desktop_path + '/mycart')
        # Überprüfung durch plone4.csrffixes sollte schon geschehen sein,
        # wenn wir hier angekommen sind:
        try:
            del form['_authenticator']
        except KeyError:
            pass
        return False

    @log_or_trace(**lot_kwargs)
    def _order_mail_subject(self,
                            hub, info,
                            order=None, config=None,
                            type='normal'):
        if order is None and not 'wieso?!':
            assert type == 'failed'
        if config is None:
            hub, info = make_hubs(self.context)
            config = self._get_subportal_config(hub, info)
        _ = make_translator(self.context)
        if 0:
            pp(order)
            set_trace()
        dic = {'subportal': config['title'],
               'ordernr': order['ordernr'],
               }
        return _(USER_MAIL_SUBJECT[type]) % dic

    @log_or_trace(**lot_kwargs)
    def _order_mail_subject__backend(self, hub, info, order, config=None):
        if config is None:
            config = self._get_subportal_config(hub, info)
        _ = hub['translate']
        dic = {'subportal': config['title'],
               'ordernr': order['ordernr'],
               'userid': order['userid']
               }
        names = ' '.join([v for v in
                          [order.get(key)
                           for key in ('firstname', 'lastname')
                           ]
                          if v])
        company = order.get('company')

        if names and company:
            userinfo = ', '.join((names, company))
        else:
            userinfo = names or company
        dic['userinfo'] = (userinfo
                           and ' (%(userinfo)s)' % locals()
                           or '')
        return _('Booking activity on %(subportal)s: '
                 'order no. %(ordernr)s '
                 'by %(userid)s%(userinfo)s'
                 ) % dic

    @log_or_trace(**lot_kwargs)
    def get_sending_mail_address(self, hub=None, info=None):
        """
        Ermittle die sendende Mail-Adresse (Subportal-Eigenschaft)
        """
        if hub is None:
            hub, info = make_hubs(self.context)
        val = hub['subportal'].get_from_address('booking_email')
        if val and isinstance(val, six_string_types):
            return val
        # Fallback: alte Variante ("Umgebungsvariable")
        conf = getConfiguration()
        env = conf.environment
        return env.get('mail_from', 'order@unitracc.de')

    @log_or_trace(**lot_kwargs)
    def make_greeting(self, order, hub=None, info=None):
        """
        order - ein dict (Datensatz aus `unitracc_orders`)
        """
        if hub is None:
	    _ = make_translator(self.context)
        else:
	    _ = hub['translate']
        raw = []
        for key in ('firstname', 'lastname'):
            val = order.get(key)
            if val:
                raw.append(val)
        if raw:
            return _('Dear ${name},',
                     mapping={'name': ' '.join(raw),
                              })
        return _('Dear Sir or Madam,')

    def _send_mail(self, template, hub, info, **kwargs):
        """
        Neue universelle Methode für Buchungsmails

        Schlüsselwortargumente:
        - orderdata - die von _get_order_articles_and_calculation
          zurückgegebenen Daten
        - to_admin -- geht die Mail an den Administrator?
        - order -- normalerweise orderdata entnommen
        - articles -- normalerweise orderdata entnommen
        - user_id -- normalerweise orderdata entnommen
        - user -- normalerweise mit Hilfe von user_id beschafft
        - greeting -- wenn nicht explizit angegeben, aus
                      den Buchungsdaten abgeleitet
        - subject_type -- 'normal', 'failed' ...
        - flash_message - soll eine Information über die versandte Mail ausgegeben werden?
                          Vorgabe: ja, wenn nicht to_admin
        """
        to_admin = kwargs.pop('to_admin', False)
        options = {
                'domain': info['portal_url'],
                'config': self._get_subportal_config(hub, info),
                }
        # fortan stets den ganzen Datensatz von -->
        # _get_order_articles_and_calculation übergeben:
        orderdata = options['orderdata'] = kwargs.pop('orderdata', {})
        order = orderdata.get('order') or kwargs.pop('order', {})
        if 0:
            set_trace()
        if order:
            # Unterstützung alter Templates:
            options['order'] = order
            options['articles'] = (orderdata.get('articles', None)
                                   or kwargs.pop('articles', None)
                                   )
        if orderdata:
            options['calculated'] = orderdata['calculated']

        val = kwargs.pop('greeting', None)
        if val is None and order and not to_admin:
            val = self.make_greeting(order, hub, info)
        options['greeting'] = val

        if to_admin:
            subject = self._order_mail_subject__backend(
                        hub, info, order, options['config'])
        else:
            subject_type = kwargs.pop('subject_type', 'normal')
            subject = self._order_mail_subject(hub, info,
                                               order,
                                               options['config'],
                                               type=subject_type)

        flash_message = kwargs.pop('flash_message',
                                   not to_admin)

        # auch als Admin-Adresse:
        mail_from = options['mail_from'] = self.get_sending_mail_address(hub, info)

        user = kwargs.get('user', None)
        user_id = kwargs.get('user_id', None)
        if user_id is None and order:
            user_id = order['userid']
        if user is None and user_id is not None:
            user = hub['author'].getByUserId(user_id)

        user_email = kwargs.pop('user_email', None)
        if user_email is None and user is not None:
            user_email = user.getEmail()
        options['user_email'] = user_email

        if to_admin:
            mail_to = mail_from
        elif user_email:
            mail_to = user_email
        else:
            raise Exception('Nix user, nix email!')

        # verbliebene Angaben weiterreichen:
        options.update(kwargs)

        mail = hub['unitraccmail']
        mail.set('utf-8', template, subject, options)
        mail.renderAsHTML()

        args = [mail, mail_from, mail_to]
        # neue kwargs, für sendMail:
        kwargs = {'subject': subject,
                  }
        if flash_message:
            kwargs['message'] = getMessenger(self.context)
        sendMail(*args, **kwargs)

    @log_or_trace(**lot_kwargs)
    def _send_success_mail(self, user, order, articles):
        """
        Versende Bestätigungsmail an Kunden: Zahlung erhalten
        wg. get_access_duration: die Methode _send_success_mail
        wird ohnehin abgelöst
        """
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        # templates/mail_order_success.pt
        template = "mail_order_success"
        hub, info = make_hubs(self.context)
        config = self._get_subportal_config(hub, info)
        subject = self._order_mail_subject(hub, info, order, config)
        mail_from = self.get_sending_mail_address(hub, info)
        # FIXME: eine Mail pro *Auftrag*, nicht pro Artikel
        mail = self.context.getBrowser('unitraccmail')
        for article in articles:
            group = learner_group_id(article['article_uid'])
            options = {'name':     user.getUserId,
                       'greeting': self.make_greeting(order),
                       'start':    article['start_ddmmyyyy'],
                       'duration': article['duration'],
                       'domain':   portal.absolute_url(),
                       }
            mail.set('utf-8', template, subject, options)
            mail.renderAsHTML()
            if debug_active:
                pp((('Mail-Template:', template),
                    ('options-dict fuer Mail:', options),
                    ('user:', user),
                    ('mail.email:', mail.email),
                    ))
        sendMail(mail, mail_from, user.getEmail(),
                 subject=subject)

    @log_or_trace(**lot_kwargs)
    def _send_pending_mail(self, user, order, articles, payment_info):
        """
        Versende Mail an Kunden: Zahlung noch nicht abgeschlossen
        """
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        # templates/mail_payment_pending.pt
        template = "mail_payment_pending"
        hub, info = make_hubs(self.context)
        config = self._get_subportal_config(hub, info)
        subject = self._order_mail_subject(hub, info, order, config)
        # subject = _("Order processing information from UNITRACC")
        mail_from = self.get_sending_mail_address(hub, info)
        options = {'name': user.getUserId,
                   'greeting': self.make_greeting(order),
                   'domain': portal.absolute_url(),
                   'payment_info': payment_info,
                   }
        mail = self.context.getBrowser('unitraccmail')
        mail.set('utf-8', template, subject, options)
        mail.renderAsHTML()
        if debug_active:
            pp((('Mail-Template:', template),
                ('options-dict fuer Mail:', options),
                ('user:', user),
                ('mail.email:', mail.email),
                ))
        return sendMail(mail, mail_from, user.getEmail(),
                        subject=subject)

    @log_or_trace(**lot_kwargs)
    def _send_backend_mail(self, user, order, articles, payment_info):
        """
        Versende Mail an Admin: Zahlungsdetails
        """
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        # templates/mail_payment_backend.pt
        template = "mail_payment_backend"
        hub, info = make_hubs(self.context)
        config = self._get_subportal_config(hub, info)
        subject = self._order_mail_subject__backend(hub, info, order, config)
        mail_from = self.get_sending_mail_address(hub, info)
        options = {'name': user.getUserId,
                   'domain': portal.absolute_url(),
                   'payment_info': payment_info,
                   'order': order,
                   }
        mail = self.context.getBrowser('unitraccmail')
        mail.set('utf-8', template, subject, options)
        mail.renderAsHTML()
        if debug_active:
            pp((('Mail-Template:', template),
                    ('options-dict fuer Mail:', options),
                    ('user:', user),
                    ('mail.email:', mail.email),
                    ))
        return sendMail(mail, mail_from, mail_from,
                        subject=subject)

    @log_or_trace(**lot_kwargs)
    def _send_fail_mail(self, user):
        """
        Mail an den Kunden: die Bezahlung ist fehlgeschlagen
        """
        # templates/mail_order_failed.pt
        template = "mail_order_failed"
        hub, info = make_hubs(self.context)
        config = self._get_subportal_config(hub, info)
        subject = self._order_mail_subject(hub, info, order, config,
                                           type='failed')
        options = {'name': user.getUserId,
                   'greeting': self.make_greeting(order),
                   }
        mail_from = self.get_sending_mail_address(hub, info)
        mail = self.context.getBrowser('unitraccmail')
        mail.set('utf-8', template, subject, options)
        mail.renderAsHTML()
        if debug_active:
            pp((('Mail-Template:', template),
                ('options-dict fuer Mail:', options),
                ('user:', user),
                ('mail.email:', mail.email),
                ))
        return sendMail(mail, mail_from, user.getEmail(),
                        subject=subject)

    @log_or_trace(**lot_kwargs)
    def _generate_ordernumber(self, sql):
        """
        private Method
        """
        # Erstellen einer Bestellnummer
        year = date.today().year
        last = self.get_last_ordernumber(sql)

        start = 1000
        if not last:
            new = "%04d" % (start + 1)
        else:
            number = last.split("-")[1]
            old = int(number)
            new = "%04d" % (old + 1)
        ordernr = "B%04d-%s" % (year, new)
        # XXX: es wird für jede Nummer eine einzelne SQL-Abfrage abgesetzt ...
        while self._ordernumber_exists(sql, ordernr):
            old = new
            new = "%04d" % (old + 1)
            ordernr = "B%04d-%s" % (year, new)
        return ordernr

    # @log_or_trace(**lot_kwargs)
    def _ordernumber_exists(self, sql, ordernumber):
        """
        private Method
        """
        for row in sql.select("unitracc_orders",
                              fields=["ordernr"],
                              query_data={'ordernr': ordernumber}):
            return True
        return False

    # @log_or_trace(**lot_kwargs)
    def can_view_booking_button(self, object_):
        """
        Bestimmt, ob der Buchungs-Button angezeigt werden soll

        Verwendet in:
        - ../../skins/unitracc_templates/course_overview.pt
        - ../../skins/unitracc_templates/unitracccourse_view.pt

        Sieh nach, ob es in der Gruppenzuordnungstabelle einen aktiven Eintrag für
        die (Lern-) Gruppe `group_id_` und den Benutzer `member_id_` gibt;
        wenn ja, gibt es keinen Buchungsbutton.
        """

        context = self.context
        ## Kostenlose Kurse brauchen nicht gebucht zu werden -
        ## auch nicht von unangemeldeten Benutzern!
        # if context.getAdapter('isanon')():
        #     return True

        usero = getToolByName(context, 'portal_membership').getAuthenticatedMember()
        user_id = usero.getId()
        portal = getToolByName(context, 'portal_url').getPortalObject()
        sm = portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()
        try:
            try:
                price = float(object_.getPrice_shop())
            except:
                price = 0.00

            if not (price and object_.getShopduration()):
                return False
        finally:
            sm.setOld()

        with self.sql as sql:
            object_uid = object_.UID()
            # gibt es eine aktive Buchung für den Kurs? dann kein Buchungsbutton
            group_id = learner_group_id(object_uid)
            # siehe neue View current_course_bookings_view
            rs = sql.select("unitracc_groupmemberships",
                            ["id"],
                            'WHERE NOW() BETWEEN start AND ends'
                             ' AND group_id_ = %(group_id)s'
                             ' AND member_id_ = %(user_id)s',
                            {'group_id': group_id,
                             'user_id': user_id,
                             })
            if len(rs):
                return False
            return True

            for dic in self._get_current_order_articles(sql)['art']:
                if dic['article_uid'] == object_uid:
                    return False
        return True

    # @log_or_trace(trace=1, **lot_kwargs)
    def save_preferences(self, backend=False):
        """
        Formularaktion für --> templates/order_preferences.pt

        Ersetzt die alte Methode save_payment
        """
        context = self.context
        hub, info = make_hubs(context)
        hub['authorized'].raise_anon()
        redirect = info['response'].redirect
        saving = info['request_var'].get('action') == 'update'
        do_save = True
        this_method = 'save_preferences'
        error_info = None
        next_page = '/order_preferences'
        ok = False
        msg_mask = ['%(this_method)s: %(error_info)s; back to %(next_page)r',
                    '%(this_method)s: ok; proceed to %(next_page)r']
        with self.sql as sql:
            result = self._get_current_order_and_choices(sql, hub, info,
                                                         silent=True,
                                                         backend=backend)
            my_keys = ['payment_type',
                       'access_settlement_mode']
            try:
                update = subdict(info['request_var'],
                                 keys=my_keys)
            except KeyError as e:
                hub['message']('Please choose!',
                               'error')
                error_info = str(e)
                logger.error(msg_mask[ok], locals())
                return redirect(tryagain_url(info['request'],
                                             my_keys,
                                             path=next_page))
            order = result['order']
            choices = result['choices']
            has_changes = False
            value_keys = {
                'payment_type': 'payment_type',
                'access_settlement_mode': 'mode_key',
                }
            for key in my_keys:
                value_key = value_keys[key]
                chosen_value = update[key]
                value_found = False
                for choice in choices[key]:
                    if (choice[value_key] == chosen_value
                        and not choice.get('disabled')
                        ):
                        value_found = True
                        break
                if not value_found:
                    hub['message']('Illegal value selected.',
                                   'error')
                    error_info = ('Unsupported value %(chosen_value)r for key %(key)r'
                                  ) % locals()
                    logger.error(msg_mask[ok], locals())
                    return redirect(tryagain_url(info['request'],
                                                 path=next_page))
                if chosen_value != order[key]:
                    has_changes = True
            # --- erstmal ohne has_changes (immer speichern):
            sql.update('unitracc_orders',
                       dict_of_values=update,
                       query_data=subdict(order, ['order_id']))
            # OK, und weiter:
            ok = True
            next_page = '/order_overview'
            logger.info(msg_mask[ok], locals())
            return redirect(tryagain_url(info['request'],
                                         ['formid'],
                                         path=next_page))

    # @log_or_trace(**lot_kwargs)
    def save_payment(self):
        """
        Formularaktion in templates/order_choose_payment_method.pt

        Bezahlungsart speichern

        Veraltet; abzulösen durch --> save_preferences
        """
        context = self.context
        portal = getToolByName(context, 'portal_url').getPortalObject()
        request = context.REQUEST
        form = request.form

        if not form.get('payment_type'):
            message(context, 'Please choose a payment method.', 'error')
            # (gf) templates/order_choose_payment_method.pt;
            # --> get_active_payment_types
            return context.restrictedTraverse('order_choose_payment_method')

        with self.sql as sql:
            hack = False
            formid = form.get('formid')
            user_id, session_id = self._get_user_and_session(context=context)

            order = self._get_order(sql, payment_status='new',
                                         sessionID=session_id,
                                         userID=user_id)
            if order is None:
                message(context,
                        '... expired',
                        'error')
                return tryagain_url(request,
                                    path='/@@our_offering')
            order_id = order['order_id']

            #------------------------------#
            # Prüfen ob der Nutzer sich    #
            # auf die Seite "gehackt" hat. #
            #------------------------------#
            hack = self.check_access()
            if hack:
                return hack

            update_ = {}
            payment_type = form['payment_type']
            if not order['paypal_allowed']:
                ppi_rows = sql.select('payment_types_view',
                                      query_data={'payment_type': payment_type})
                if not ppi_rows:  # eher theoretische Möglichkeit
                    message(context,
                            'Invalid form data!', 'error')
                    return context.restrictedTraverse('order_choose_payment_method')
                elif ppi_rows[0]['payment_type'] == 'paypal':
                    message(context,
                            'PayPal payment is disabled!', 'error')
                    return context.restrictedTraverse('order_choose_payment_method')

            sql.update("unitracc_orders",
                       {'payment_type': payment_type},
                       query_data={'order_id': order_id})

            #------------------------#
            # Prozessieren der Daten #
            #------------------------#
            hashed = make_secret(order_id)
            url_ = context.absolute_url() + '/order_overview?formid=%s' % hashed
            return request.RESPONSE.redirect(url_)

    def get_agb_link(self):
        if AGB_UID is None:
            return None

        context = self.context
        rc = getToolByName(context, 'reference_catalog')
        object_ = rc.lookupObject(AGB_UID)
        return object_.absolute_url()

    def get_paypal_langcode(self, context):
        langcode = getActiveLanguage(context)
        return paypal_langcode(langcode)

    def _get_subportal_config(self, hub, info):
        """
        Lies die Subportal-Konfigurationsdaten aus
        """
        return hub['subportal'].get_current_info()

    @log_or_trace(trace=0, **lot_kwargs)
    def get_paypal_button(self, dict_):
        """
        Erzeuge ein Formular mit dem PayPal-Bezahlknopf;
        siehe (gf) templates/paypal_button.pt
        """

        context = self.context

        # für PayPal-URL jedenfalls benötigt:
        hub, info = make_hubs(self.context)
        config = self._get_subportal_config(hub, info)

        order = dict_['order']
        articles = dict_['articles']

        # la_LA = self.get_paypal_langcode(context)
        kwargs = {
            'url':      config.get('paypal_url'),
            'title':    u', '.join([article['article_title']
                                    for article in articles
                                    ]),
            'value':    order['total'],
            'formid':   order['formid'],
            'business': order.get('paypal_id') or
                       config.get('paypal_id'),
            'order_id': order['order_id'],
            'img_src':  ('https://www.paypalobjects.com/%s'
                         '/i/btn/btn_buynow_LG.gif'
                         ) % (self.get_paypal_langcode(context),
                              ),
            }
        return context.restrictedTraverse('paypal_button')(**kwargs)

    @log_or_trace(**lot_kwargs)
    def paypal_finished(self):
        """
        Verborgenes Formularfeld "notify_url" in templates/paypal_button.pt

        Verarbeite die Antwort von PayPal:
        - Aufbereitung der Daten
        - Aufruf von _update_order_payment
          - dort ggf. Freigabe und Versand von Mails
        """
        context = self.context
        form = context.REQUEST.form
        with self.sql as sql:
            try:
                DEBUG('paypal_finished; Formulardaten:\n%s', pformat(form))

                # form-dict wird noch für INSERT verwendet:
                order_id = form['unitracc_orders_id'] = form['item_number']
                # Es wird ' PST' bzw. ' PDT' abgeschnitten.
                # TODO: Saubere Methode verwenden!
                payment_date = form['payment_date'][:-4]

                timezone_pst = pytz.timezone('America/Los_Angeles')
                timezone_eb = pytz.timezone('Europe/Berlin')
                date_time = datetime.strptime(payment_date, '%H:%M:%S %b %d, %Y')
                DEBUG('vor Kuerzung um 6 Zeichen: %s',  # '+02:00' o. ä.
                      str(timezone_pst.localize(date_time)
                          .astimezone(timezone_eb)
                          ))
                form['payment_date'] = str(timezone_pst.localize(date_time)
                                           .astimezone(timezone_eb)
                                           )[:-6]

                order = sql.select('unitracc_orders',
                                   query_data={'order_id': order_id,
                                               })[0]
                userBrowser = context.getBrowser('author')
                user = userBrowser.getByUserId(order['userid'])
                status = PAYPAL2UNITRACC_STATUS.get(form['payment_status'], 'unknown')
                self._update_order_payment(sql, user, status, order_id, backend=False)

            finally:
                dict_of_values = {}
                charset = form.pop('charset')
                logger.info('paypal_finished: Formularfelder %s', (list(dict_of_values.keys()),))
                for key, val in form.items():
                    dict_of_values[key] = val.decode(charset)  # charset aus PayPal-Antwort
                    logger.info('paypal_finished, %s: %r', key, dict_of_values[key])

                DEBUG('Daten fuer unitracc_orders_paypal:\n%s',
                      pformat(dict_of_values))
                sql.insert('unitracc_orders_paypal', dict_of_values)

                return 'ok'

    def get_paypal_payment_states(self):

        return PAYPAL_PAYMENT_STATES

    @log_or_trace(**lot_kwargs)
    def get_paypal_history_by_order_id(self, order_id):
        """
        Verwendet in:
        - templates/order_payment_finished.pt
        - templates/order_edit.pt
        - templates/order_view.pt

        unitracc_orders_paypal.item_number: VARCHAR(100)
        """
        with self.sql as sql:
            list_ = list(sql.query("""
                SELECT * FROM unitracc_orders_paypal
                 WHERE item_number = %(item_number)s
                 ORDER BY item_number DESC;
                 """,
                 query_data={'item_number':
                             order_id,
                             }))
            return list_

    def get_paypal_urls(self):
        """
        Gib die Liste der erlaubten PayPayl-URLs zurück
        """
        return ['https://www.sandbox.paypal.com/de/cgi-bin/webscr',
                'https://www.paypal.com/de/cgi-bin/webscr',
                ]
