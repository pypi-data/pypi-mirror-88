# -*- coding: utf-8 -*- äöü
"""
Browser unitracc@@tan: Zugangscodes (Transaktionsnummern, TANs) verwalten
"""
# Python compatibility:
from __future__ import absolute_import, print_function

from six import string_types as six_string_types
from six.moves import map, range

# Standard library:
from codecs import BOM_UTF8
from csv import excel, register_dialect
from csv import writer as csv_writer
from datetime import date
from pprint import pformat
from random import choice, shuffle
from time import strftime

# Zope:
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName

# 3rd party:
import StringIO

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.base.permissions import CREATE_TAN as PERM_CREATE_TAN
from visaplan.plone.base.permissions import MANAGE_TANS
from visaplan.plone.base.permissions import MANAGE_TANS as PERM_MANAGE_TANS
from visaplan.plone.base.permissions import VIEW_TANS as PERM_VIEW_TANS
from visaplan.plone.groups.groupsharing.browser import (
    groupinfo_factory,
    is_direct_member__factory,
    )
from visaplan.plone.tools.context import make_translator
from visaplan.plone.tools.forms import merge_qvars, tryagain_url
from visaplan.tools.classes import Mirror
from visaplan.tools.coding import make_safe_stringrecoder
from visaplan.tools.csvfiles import make_sequencer
from visaplan.tools.dates import parse_date
from visaplan.tools.dicts import make_key_injector, subdict
from visaplan.tools.minifuncs import translate_dummy as _
from visaplan.tools.sql import make_where_mask, subdict_ne

# Local imports:
from .utils import (
    DATE_FORMAT,
    TAN_EXAMPLE,
    check_tan,
    date_as_string,
    default_duration,
    default_expiration_date,
    )
from .utils import group3 as format_tan
from .utils import (
    invalid_tan_txt,
    start_and_ends,
    start_and_ends2,
    tan2int,
    today_matches_spec,
    )

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import log_or_trace, make_sleeper, pp

LOGGER, debug_active, DEBUG = getLogSupport('tan')

lot_always = {'debug_level': True,
              'logger': LOGGER,
              'log_result': True,
              'result_formatter': str,
              }

sleep = make_sleeper(LOGGER, default=1.5)
DEBUG_PERMISSIONS = debug_active

# ----------------------------------------------[ für den Parser ... [
#            (Markierung mit ""-Präfix funktioniert nicht zuverlässig)
STATUS_ERROR_TEXT = {'used':    _('The TAN %(tan)s has already been used.'),
                     'expired': _('The TAN %(tan)s has expired.'),
                     'deleted': _('The TAN %(tan)s was deleted.'),
                     }
# ----------------------------------------------] ... für den Parser ]

STATUS_USABLE = ['new', 'reserved']
STATUS_UNUSABLE = ['used', 'expired', 'deleted']
assert set(STATUS_UNUSABLE) == set(STATUS_ERROR_TEXT.keys())

# siehe tans_wizard.pt, tan_view, sorted_columns
COLUMNS_SEQUENCE = {}
COLUMNS_ORDER = {
        'checkbox':           10,
        'changeset':          20,
        'quantity':           30,
        'tan':                40,
        'status':             50,
        'group_title':        59,
        'pretty_title':       59,
        'Group':              60,
        'group_id':           60,
        'duration_days':      70,
        'owner_id':           80,    # redeemed_by
        'additional_info':    90,
        'expiration_date':   100,
        'changed_by':        110,
        'last_changed_date': 120,
        }


class ExcelSSV(excel):
    """
    Der Standard-"Excel-Dialekt" des csv-Moduls verwendet Kommas
    """
    delimiter = ';'
register_dialect('excel_ssv', ExcelSSV)


class ITan(Interface):
    """
    Interface zur Verwaltung von TANs
    """
    # def tan_csv_export: siehe ../../skins/unitracc_templates/tan_csv_export.py,
    # verwendet --> csv_export --> _export_as_csv

    def canCreate():
        """
        Darf der angemeldete Benutzer hier TANs erzeugen?
        """

    def canView():
        """
        Darf der angemeldete Benutzer hier TANs sehen?
        """

    def canManage():
        """
        Darf der angemeldete Benutzer hier TANs verwalten?
        """

    def authCreate():
        """
        Darf der angemeldete Benutzer hier TANs erzeugen?
        (wirft ggf. eine Unauthorized-Exception)
        """

    def authView():
        """
        Darf der angemeldete Benutzer hier TANs sehen?
        (wirft ggf. eine Unauthorized-Exception)
        """

    def authManage():
        """
        Darf der angemeldete Benutzer hier TANs verwalten?
        (wirft ggf. eine Unauthorized-Exception)
        """

    def change():
        """
        Allgemeine Änderungen an einer TAN;
        zum Einlösen gibt es die dedizierte Methode --> redeem.
        """

    def redeem():
        """
        Löse die übergebene TAN ein
        """

    def list(sql=None):
        """
        Liste die TANs gem. dem gegebenen Filter auf
        """

    def history(sql=None):
        """
        Liste die TANs gem. dem gegebenen Filter auf
        """

    def addTAN():
        """
        Formularaktion zum Erzeugen einer TAN
        """

    def get_groupinfo(group_id):
        """
        Für Formulare: Basisinformationen über eine einzelne Gruppe
        besorgen
        """

    def get_frequent_filter_names():
        """
        Die Namen häufig benutzter Filterfelder
        """

    def get_all_fields():
        """
        Alle Namen, die bei Bearbeitung benoetigt werden
        """

    def csv_export():
        """
        Exportiere eine TAN-Liste gemäß den aktuellen Filterkritien
        """

    def expire():
        """
        Abgelaufene TANs deaktivieren
        """

    def auth_unitracc_manage_tans():
        """ """

    def tan_example():
        """
        Beispielhafter Wert, z. B.  '123.456.789'
        """

    def formdata():
        """
        Formulardaten; Feldvorbelegungen
        """

# nicht in tan_history oder tan_changeset protokolliert:
TAN_FIELDS_UNTRACKED = ['group_id', 'duration_days', 'expiration_date']
TAN_FIELDS_CHANGEABLE = ['status', 'owner_id',
                         'additional_info',
                         ] + TAN_FIELDS_UNTRACKED
TAN_FIELDS = ['tan',  # 'tan_stem'
              ] + TAN_FIELDS_CHANGEABLE
FREQUENTLY_USED_FILTERS = ['group_id', 'status', 'changeset']
# Mapping von Formular-Schlüsseln zu SQL-Feldnamen:
FORM2SQL = Mirror()
# FORM2SQL['gid'] = 'group_id'
# Gegenstück (TODO: automatischer Abgleich):
# SQL-Feldnamen zu Formular-Schlüsseln
SQL2FORM = Mirror()
# SQL2FORM['group_id'] = 'gid'


class Browser(BrowserView):

    implements(ITan)

    def can(self, perm):
        context = self.context
        if DEBUG_PERMISSIONS:
            LOGGER.info('Checking %r permission ...', perm)
            ok = getToolByName(context, 'portal_membership').checkPermission(perm)
            LOGGER.info('%r permission: %s', perm, ok and 'OK' or 'missing!')
            return ok
        return getToolByName(context, 'portal_membership').checkPermission(perm, context)

    def canCreate(self):
        """
        Darf der angemeldete Benutzer hier TANs erzeugen?
        """
        return self.can(PERM_CREATE_TAN)

    def canView(self):
        """
        Darf der angemeldete Benutzer hier TANs sehen?
        """
        return self.can(PERM_VIEW_TANS)

    def canManage(self):
        """
        Darf der angemeldete Benutzer hier TANs verwalten?
        """
        return self.can(PERM_MANAGE_TANS)

    def canManageThis(self):
        """
        Darf der angemeldete Benutzer *diese* TAN verwalten?
        """
        context = self.context
        pm = getToolByName(context, 'portal_membership')
        if pm.isAnonymousUser():
            raise Unauthorized

        if self.can(PERM_MANAGE_TANS):
            return True

        form = context.form
        # Wer sie erzeugt hat, darf sie nicht mehr unbedingt verwalten;
        # es kommt darauf an, ob er noch Gruppenadministrator ist:
        tan = form.get('tan')
        if tan:
            try:
                stem = check_tan(tan)
            except ValueError:
                LOGGER.error('Invalid tan %(tan)r', locals())
                return False
            else:
                with context.getAdapter('sqlwrapper') as sql:
                    row = sql.select('tan',
                                     query_data={'tan_stem': stem})
                    group_id = row['group_id']
                    usermanagement = context.getBrowser('usermanagement')
                    return usermanagement.is_group_manager(group_id)

    def auth(self, perm):
        """
        wirf eine Unauthorized-Exception, wenn die übergebene Berechtigung fehlt
        """
        if not self.can(perm):
            if DEBUG_PERMISSIONS:
                LOGGER.info('raising Unauthorized!')
            raise Unauthorized

    def authCreate(self):
        """
        Darf der angemeldete Benutzer hier TANs erzeugen?
        (wirft ggf. eine Unauthorized-Exception)
        """
        if not self.canCreate():
            raise Unauthorized

    def authView(self):
        """
        Darf der angemeldete Benutzer hier TANs sehen?
        (wirft ggf. eine Unauthorized-Exception)
        """
        if not (self.canView() or self.canManageThis()):
            raise Unauthorized

    def authManage(self):
        """
        Darf der angemeldete Benutzer hier TANs verwalten?
        (wirft ggf. eine Unauthorized-Exception)
        """
        if not self.canManage():
            raise Unauthorized

    def authManageThis(self):
        """
        Darf der angemeldete Benutzer *diese* TAN verwalten?
        (wirft ggf. eine Unauthorized-Exception)
        """
        if not self.canManageThis():
            raise Unauthorized

    @staticmethod
    def _new_changeset_id(sql, user_id):
        """
        Erzeuge einen neuen Änderungssatz und gib seine ID zurück
        """
        inserted1 = sql.insert('tan_changeset',
                               {'user_id': user_id,
                                },
                               returning='id')
        for dic in inserted1:
            return dic['id']
        raise ValueError('Creation of changeset row failed!')

    def addTAN(self):
        """
        Erzeuge eine oder mehrere TANs und gib die Nummer des
        Änderungssatzes zurück

        Formular (gf): templates/create_tan.pt
        """
        context = self.context

        self.auth_unitracc_manage_tans()

        # Daten:
        request = context.REQUEST
        redirect = request.RESPONSE.redirect
        form = request.form
        pm = getToolByName(context, 'portal_membership')
        auth_member = pm.getAuthenticatedMember()
        creator = str(auth_member)
        try:
            # Kopie übergeben, wg. tryagain_url:
            tan_data = self._tans_data(form)
            self._apply_tans_defaults(tan_data)
            error_url = tryagain_url(request, list(tan_data.keys()))
            self._check_newtan_data(tan_data)
            quantity = int(form.get('quantity', 1))
            with context.getAdapter('sqlwrapper') as sql:
                # Hilfstabelle für Zusammenfassung von Sammelaufträgen:
                changeset = self._new_changeset_id(sql, creator)
                tans = []
                for i in range(quantity):
                    for row in sql.insert('tan',
                                          tan_data,
                                          returning=('tan', 'status')):
                        tans.append(dict(row))
                        tan = row['tan']
                        LOGGER.info('TAN %(tan)r erzeugt', locals())
                        sql.insert('tan_history',
                                   {'tan': tan,
                                    'changeset': changeset,
                                    'status': row['status'],
                                    })

            kwargs = {}
            kwargs['changeset'] = changeset
            kwargs['gid'] = form.get('gid')

            url = merge_qvars(context.absolute_url() + '/manage_tans', kwargs)

            return redirect(url)

        except ValueError as e:
            message(context, str(e), 'error')
            return request.RESPONSE.redirect(tryagain_url(request, list(tan_data.keys())))
        except Exception as e:
            message(context,
                    '\n'.join((e.__class__.__name__,
                               str(e),
                               '(@@tan:381)')), 'error')
            print(' -*- '.join(['381'] * 10))
            print(e.__class__.__name__)
            print(str(e))
            print(' -*- '.join(['381'] * 10))
            return request.RESPONSE.redirect(tryagain_url(request, list(tan_data.keys())))

    def _redeem2(self, tan, owner_id, start,
                 sql, **kwargs):
        """
        Arbeitspferd für Methode _redeem (und nur durch diese aufzurufen!)

        Löse die übergebene TAN ein;
        Fehlerbehandlung per Exceptions (ValueError).

        tan - die TAN (Zugangscode, der die Mitgliedschaft
              zu einer Gruppe vermittelt)
        owner_id - die ID des einlösenden Benutzers
        start - ein Startdatum, oder None (heute)
        sql - der Datenbankadapter (Context manager)

        Gib einen String zurück, der als Nachricht ausgegeben werden kann.
        """
        assert isinstance(tan, int), \
                ('Typpruefung der TAN in aufrufendem _redeem (%(tan)r)'
                 ) % locals()
        query_data = {'tan': tan,
                      }
        rows = sql.select('tan',
                          query_data=query_data)
        context = self.context
        _ = make_translator(context)  # ggf. auch den Import wieder löschen
        if not rows:
            raise ValueError(invalid_tan_txt(tan, _))
        row = rows[0]
        # TODO: - bei Status 'reserved' nur einlösbar, wenn die ID
        #         des nutznießenden Benutzers eingetragen ist
        #       - Güteschutz: wenn gsmember_id in TAN vermerkt,
        #         muß diese mit der angegebenen Mitgliedsnummer übereinstimmen
        #       - eine bestehende Mitgliedschaft darf durch eine TAN nicht verkürzt,
        #         eine unbefristete nicht befristet werden!
        self._check_tan_availability(**row)

        gs = context.getBrowser('groupsharing')
        group_info = gs.get_group_info_by_id(row['group_id'],
                                             pretty=1, getObject=1)
        if not group_info:
            raise ValueError(_('No group "%(group_id)s" found!') % row)
        # das Objekt:
        group_object = context.getBrowser('groups').getById(row['group_id'])
        if 0:\
        pp((('group_object:', group_object),
            ('group_info:', group_info),
            ))
        data = {'group_id_':  row['group_id'],
                'member_id_': owner_id,
                }
        groups_update = start_and_ends2(start, row['duration_days'])
        data.update(groups_update)
        # nicht Bestandteil der Stammdaten (tan-Tabelle):
        changeset = self._new_changeset_id(sql, owner_id)

        # ------------------------- [ TAN jedenfalls verbrauchen ... [
        new_data = dict(kwargs)  # z. B. Güteschutz-Mitgliedsnummer
        new_data.update({'status': 'used',
                         'owner_id': owner_id,
                         })
        # nun in Datenbank schreiben:
        sql.update('tan',
                   new_data,
                   where=make_where_mask(query_data),
                   query_data=query_data,
                   commit=False)
        sql.insert('tan_history',
                   {'status': 'used',
                    'tan': tan,
                    'owner_id': owner_id,
                    'changeset': changeset,
                    },
                   commit=False)
        # ------------------------- ] ... TAN jedenfalls verbrauchen ]
        # siehe @@groupsharing.add_to_group:
        query_data = {'done': False,
                      }
        query_data.update(data)
        rows = sql.select('unitracc_groupmemberships',
                          fields=('start', 'ends', 'active',
                                  'id'),
                          query_data=query_data)
        doit = False       # True --> insert
        query_data = None  # wenn nicht None --> Update
        if rows:
            unlimited = False
            # Annahme: es gibt nur einen entscheidenden Datensatz;
            #          dieser wird ggf. geändert
            for row in rows:
              try:
                # data: datetime.date, z. B. datetime.date(2016, 2, 16);
                # row: DateTime, z. B. DateTime('2016/02/16 00:00:00 GMT+0')
                row_start =  date_as_string(row['start'])
                row_ends =   date_as_string(row['ends'])
                data_start = date_as_string(data['start'])
                data_ends =  date_as_string(data['ends'])
                if row_ends is None:
                    # Unbegrenzte Mitgliedschaft schon eingepflegt
                    if data_ends < row_start:
                        # Neues Ende vor aktuellem Start:
                        doit = True  # insert
                    elif data_start < row_start:
                        # Aktueller Start wird vorgezogen:
                        # bisherigen Datensatz ändern,
                        query_data = subdict(row, ['id'])
                        # Endedatum erhalten:
                        data['ends'] = row['ends']
                    else:
                        # Neuer Start nach aktuell schon vorhandenem
                        break
                # Bisheriger Eintrag ist begrenzt.
                elif data_ends is None:
                    # Der neue Eintrag ist unbegrenzt:
                    if data_start <= row_ends:
                        query_data = subdict(row, ['id'])
                        if data_start > row_start:
                            data['start'] = row['start']
                    else:
                        doit = True
                else:
                    # Alles ist begrenzt
                    LOGGER.info('data = %s;\nrow = %s',
                                pformat(data), pformat(row))
                    if row_start <= data_start <= row_ends:
                        # Start fällt in den schon gebuchten Zeitraum
                        if data_ends is None:
                            # Neue Mitgliedschaft unbegrenzt
                            query_data = subdict(row, ['id'])
                            data['start'] = row['start']
                        elif data_ends <= row_ends:
                            # Neue Mitgliedschaft in gebuchter enthalten
                            break
                        else:
                            query_data = subdict(row, ['id'])
                            data['start'] = row['start']
                    elif row_start <= data_ends <= row_ends:
                        # Ende fällt in den schon gebuchten Zeitraum;
                        # der Start liegt davor
                        assert data_start < data_ends
                        query_data = subdict(row, ['id'])
                        data['ends'] = row['ends']
                    else:
                        # keine Überschneidung, kein Anschluß
                        doit = True
                break
              except (TypeError, ValueError) as e:
                  LOGGER.error('\ndata = %s;\nrow = %s',
                               pformat(data), pformat(row))
                  LOGGER.exception(e)
                  raise
        else:
            doit = True

        if query_data is not None:
            sql.update('unitracc_groupmemberships',
                       data,
                       query_data=query_data,
                       commit=False)
        elif doit:
            sql.insert('unitracc_groupmemberships',
                       data,
                       commit=False)
        pretty = format_tan(tan)
        msglist = [_('Thank you!'),
                   _('TAN %(pretty)s was redeemed successfully.'
                     ) % locals(),
                   ]

        def use_pretty(dic):
            # bezieht sich auf die Gruppenbezeichnung
            return ('pretty_title' in dic
                    and dic['pretty_title']
                    and dic['pretty_title'] != dic['group_title']
                    )

        TODAY = date.today()
        if today_matches_spec(data, TODAY):
            group_object.addMember(owner_id)
            msglist.append(
                (use_pretty(group_info)
                 and _('You are now member of the %(pretty_title)s.')
                  or _('You are now member of the "%(group_title)s" group.')
                 ) % group_info)
        else:
            if '%' in group_info['pretty_title']:
                group_info['pretty_title'] = \
                        group_info['pretty_title'].replace('%', '%%')
            msglist.append(
                data['start'].strftime(
                    (use_pretty(group_info)
                     and _('Your membership in the %(pretty_title)s '
                           'will start on %%d.%%m.%%Y.')
                      or _('Your membership in the "%(group_title)s" group '
                           'will start on %%d.%%m.%%Y.')
                     ) % group_info))

        if 'ends' in data and data['ends'] is not None:
            msglist.append(
                data['ends'].strftime(_(
                    'The membership will expire on %d.%m.%Y.'
                    )))
        return '\n'.join(msglist)

    def _redeem(self, tan, owner_id, start=None,
                sql=None,
                **kwargs):
        """
        Löse die übergebene TAN ein;
        Fehlerbehandlung per Exceptions (ValueError).

        Argumente:
        tan - die TAN (Zugangscode, der die Mitgliedschaft
              zu einer Gruppe vermittelt)
        sql - kann übergeben werden, wenn im Kontext schon beschafft,
              und wird ansonsten nach Vorprüfung selbst ermittelt

        ... ansonsten siehe _redeem2.

        Generiere Strings (oder Dicts?) zur Ausgabe von Nachrichten
        """
        tan = check_tan(tan, nonempty=True, complete=True,
                        calling_self=self)
        if not owner_id:
            raise ValueError('No owner specified!')
        if sql is None:
            with self.context.getAdapter('sqlwrapper') as sql:
                return self._redeem2(tan, owner_id, start,
                                     sql,
                                     **kwargs)
        return self._redeem2(tan, owner_id, start,
                             sql,
                             **kwargs)

    def redeem(self):
        """
        Löse die per Formulardaten übergebene TAN ein
        """
        context = self.context
        request = context.REQUEST
        pm = getToolByName(context, 'portal_membership')
        if pm.isAnonymousUser():
            raise Unauthorized
        error_path = tryagain_url(request, ('tan', 'start'))
        redirect = request.RESPONSE.redirect
        auth_member = pm.getAuthenticatedMember()
        owner_id = str(auth_member)
        form = request.form
        tan = form.get('tan', None)
        try:
            msg = self._redeem(tan, owner_id, form.get('start'))
            if msg:
                message(context, msg)
        except ValueError as e:
            message(context, str(e), 'error')
            return redirect(error_path)

        desktop_path = context.getBrowser('unitraccfeature').desktop_path()
        return redirect(desktop_path)

    def change(self):
        """
        Allgemeine Änderungen an einer TAN;
        zum Einlösen gibt es die dedizierte Methode --> redeem.
        """
        context = self.context
        request = context.REQUEST
        self.authManage()
        error_path = tryagain_url(request, TAN_FIELDS)
        pm = getToolByName(context, 'portal_membership')
        auth_member = pm.getAuthenticatedMember()
        owner_id = str(auth_member)
        redirect = request.RESPONSE.redirect
        _ = make_translator(context)  # ggf. auch den Import wieder löschen
        try:
            values_for_tan = self._tans_data()
            # Hier kein subdict_ne, weil 'tan' wirklich vorhanden
            # sein muß!
            tan = values_for_tan.pop('tan')
            query_data = {'tan': tan}
            if not values_for_tan:
                raise ValueError(_('Nothing to do!'))
            with context.getAdapter('sqlwrapper') as sql:
                changeset = self._new_changeset_id(sql, owner_id)
                rows = list(sql.select('tan',
                                       query_data=query_data))
                if not rows:
                    raise ValueError(_('TAN %(tan)s not found!'
                                       ) % query_data)
                old_values = rows[0]
                rows = sql.update('tan',
                                  values_for_tan,
                                  query_data=query_data,
                                  returning=['tan', 'status'])
                new_values = list(rows)[0]
                values_for_changeset = subdict_ne(values_for_tan,
                                                  ['additional_info'])
                if values_for_changeset:
                    sql.update('tan_changeset',
                               values_for_changeset,
                               query_data={'id': changeset})
                untracked = subdict_ne(values_for_tan,
                                       TAN_FIELDS_UNTRACKED,
                                       pop=1)
                values_for_history = {'tan': tan,
                                      'changeset': changeset,
                                      }
                values_for_history.update(values_for_tan)

                if not 'status' in values_for_history:
                    values_for_history['status'] = new_values['status']
                sql.insert('tan_history',
                           values_for_history)
                message(context,
                        _('Changes saved in changeset #%(changeset)d'
                          ) % locals(),
                        'info')
                return redirect(tryagain_url(request, ['tan']))
        except KeyError as e:
            print(e.__class__, e)
            message(context,
                    ""'No TAN given!', 'error')
            return redirect(error_path)
        except ValueError as e:
            message(context, str(e), 'error')
            return redirect(error_path)

    def _check_tan_availability(self, status, tan, **kwargs):
        """
        Prüfe, ob die TAN eingelöst werden kann,
        und wirf ggf. einen ValueError
        """
        # XXX diese Methode kann ihrer Signatur nach TANs des Status
        #     'reserved' nicht auf Reservierung für nutznießenden Benutzer
        #     prüfen!
        if status in STATUS_USABLE:
            return True
        _ = make_translator(self.context)  # ggf. auch den Import wieder löschen
        txt = STATUS_ERROR_TEXT[status]
        raise ValueError(_(txt) % locals())

    def defaults(self):
        """
        Vorgabewerte für das Hinzufügen einer TAN;
        zum Füllen des Formulars
        """
        context = self.context
        form = context.REQUEST.form
        res = {}
        # -------------------- Anzahl zu generierender TANs:
        key = 'quantity'
        try:
            res[key] = int(form[key])
        except (KeyError, ValueError):
            res[key] = 1
        # ----------------------------- Dauer der Zuweisung:
        key = 'duration_days'
        try:
            res[key] = int(form[key])
        except (KeyError, ValueError):
            res[key] = default_duration()
        # ------------------------------------- Ablaufdatum:
        key = 'expiration_date'
        try:
            val = parse_date(form[key])
            res[key] = val.strftime(DATE_FORMAT)
        except (KeyError, ValueError):
            res[key] = default_expiration_date(DATE_FORMAT)
        # ----------------------------------------- Gruppen:
        key = 'group_id'
        group_id = form.get(key, None)
        if group_id is None:
            group_id = form.get('gid', None)
        res[key] = group_id
        gs = context.getBrowser('groupsharing')
        key = 'groups'
        res[key] = gs.get_manageable_groups(group_id)
        # ------------------------------------------ Status:
        key = 'status'
        res[key] = form.get(key, 'new')
        if res[key] not in STATUS_USABLE:
            res[key] = 'new'
        return res

    def _list_tans(self):
        """
        Gib die TANs gemäß den per Formular bzw. Query-String
        übergebenen Filterkriterien zurück; vorerst ist das einzige
        unterstützte Kriterium der Änderungssatz aus der Tabelle
        tan_changeset.
        """
        # TODO: Generische Joins und WHERE-Bedingungen, in Abhängigkeit
        #       von den tatsächlich angegebenen Informationen

        # context = self.context
        # pm = getToolByName(context, 'portal_membership')
        # member = pm.getAuthenticatedMember()
        # user_id = str(member)
        return self.list()

    def list_tans_pretty(self):
        """
        Wie list_tans, aber ergänze für jede gefundene Gruppe den
        Gruppentitel
        """
        pretty = True
        unique = 1
        group_title = (pretty and 'pretty_title'
                              or  'group_title')
        ggibi = groupinfo_factory(self.context, pretty=pretty)
        context = self.context
        _ = make_translator(context)  # ggf. auch den Import wieder löschen
        extend = make_key_injector('group_id',
                              ggibi,
                              group_title,
                              _('Unknown or deleted group "{group_id}"'))
        if unique:
            # Duplikate bereinigen
            latest = {}
            dupes = 0
            for row in self._list_tans():
                tan = row['tan']
                if tan in latest:
                    if row['last_changed_date'] <= latest[tan]['last_changed_date']:
                        continue
                    dupes += 1
                extend(row)
                row['group_title'] = row[group_title]
                latest[tan] = row
            if dupes:
                LOGGER.info('list_tans_pretty: %d Duplikate'
                            % (dupes,))
            elif 1:
                LOGGER.info('list_tans_pretty: keine Duplikate')
            res = []
            for tan, row in latest.items():
                key = (row['last_changed_date'],)
                res.append((key, row))
            res.sort(reverse=True)
            for tup in res:
                yield tup[1]
        else:
            if pretty:
                for row in self._list_tans():
                    extend(row)
                    row['group_title'] = row[group_title]
                    yield row
            else:
                for row in self._list_tans():
                    extend(row)
                    yield row

    def _tans_with_status(self, status, sql):
        return sql.query('''
            SELECT * FROM tan
            WHERE status IN %(status)s;
            ''',
            query_data={'status': status})

    def tans_with_status(self, status, sql=None):
        """
        TANs mit einem bestimmten Status, oder einem Status aus einer
        Liste
        """
        if isinstance(status, six_string_types):
            status = [status]
        if sql is not None:
            return self._tans_with_status(status, sql)
        with self.context.getAdapter('sqlwrapper')() as sql:
            return self._tans_with_status(status, sql)

    def tans_unused(self, sql=None):
        """
        TANs, die noch nicht eingelöst wurden
        """
        return self.tans_with_status(STATUS_USABLE, sql)

    def tans_unusable(self, sql=None):
        """
        TANs, die nicht mehr eingelöst werden können
        """
        return self.tans_with_status(STATUS_UNUSABLE, sql)

    def changeset_info(self):
        """
        Gib die Eigenschaften des angegebenen Änderungssatzes zurück
        """
        self.authView()
        context = self.context
        pm = getToolByName(context, 'portal_membership')
        member = pm.getAuthenticatedMember()
        user_id = str(member)
        form = context.REQUEST.form
        changeset = form.get('changeset', None)
        if changeset is None:
            return []   # bisher nur für Changesets
        with context.getAdapter('sqlwrapper') as sql:
            query_data = {'changeset': changeset}
            cs_rows = sql.select('tan_changeset',
                                 where='WHERE id = %(changeset)s',
                                 query_data=query_data)
            cs_info = cs_rows[0]
            if cs_info['user_id'] != user_id:
                if not self.canManage():
                    raise Unauthorized('Auf diese Daten haben Sie keinen Zugriff!')
            return cs_info

    def get_groupinfo(self, group_id):
        """
        Für Formulare: Basisinformationen über eine einzelne Gruppe
        besorgen
        """
        ggibi = groupinfo_factory(self.context, pretty=True)
        return ggibi(group_id)

    def changesets_info(self):
        """
        Variable Parameter aus Formulardaten:

        - group_id, Fallback: gid (optional)
        - user_id (optional)
        """
        self.authView()
        context = self.context
        pm = getToolByName(context, 'portal_membership')
        member = pm.getAuthenticatedMember()
        user_id = str(member)
        form = context.REQUEST.form
        group_id = form.get('group_id') or form.get('gid')
        admin_id = form.get('user_id')
        # TAN-Manager dürfen *alle* Änderungssätze sehen,
        # Normalsterbliche nur die eigenen:
        if not self.canManage():
            if admin_id:
                if admin_id != user_id:
                    # print '%(admin_id)s != %(user_id)s, und kein TAN-Manager'
                    raise Unauthorized('Auf diese Daten haben Sie keinen Zugriff!')
            else:
                admin_id = user_id
        query_data = {}
        if group_id:
            query_data['group_id'] = group_id
        if admin_id:
            query_data['user_id'] = admin_id
        with self.context.getAdapter('sqlwrapper')() as sql:
            return sql.select('tan_changesets_view',
                              query_data=query_data)

    def changesets_info_pretty(self):
        """
        rufe changesets_info auf und ergänze die Informationen um die
        Gruppentitel
        """
        grouptitles = {}
        _ = make_translator(self.context)
        ggibi = groupinfo_factory(self.context, pretty=True, forlist=1)
        for dic in self.changesets_info():
            gid = dic['group_id']
            try:
                gt = grouptitles[gid]
            except KeyError:
                minidic = ggibi(gid)
                if minidic:
                    gt = minidic['group_title']
                else:
                    gt = _('Unknown or deleted group "{group_id}"').format(**dic)
                grouptitles[gid] = gt
            dic['group_title'] = gt
            yield dic

    def _tan_statuus(self, sql):
        return sql.select('tan_status_view')

    def tan_statuus(self, sql=None):
        """
        Gib die Tabelle der möglichen Statuswerte zurück
        """
        if sql is not None:
            return self._tan_statuus(sql)
        with self.context.getAdapter('sqlwrapper')() as sql:
            return self._tan_statuus(sql)

    def _tan_status_summary(self, sql):
        return sql.select('tan_status_summary_view')

    def tan_status_summary(self, sql=None):
        """
        Gib die Tabelle der verwendeten Statuswerte mit der jeweiligen Anzahl zurück
        """
        if sql is not None:
            return self._tan_status_summary(sql)
        with self.context.getAdapter('sqlwrapper')() as sql:
            return self._tan_status_summary(sql)

    def tan_info(self):
        """
        Informationen über die aktuell bearbeitete TAN (für Breadcrumbs)
        """
        context = self.context
        tan = context.REQUEST.form.get('tan')
        try:
            tan = tan2int(tan)
        except ValueError:
            return
        with context.getAdapter('sqlwrapper')() as sql:
            query_data = {'tan': tan}
            rows = sql.select('tan', query_data=query_data)
            if not rows:
                return None
            current = rows[0]
            current['Pretty_TAN'] = format_tan(tan)
            return current

    def tan_values_and_history(self):
        """
        Gib die aktuellen Werte und die Historie der TAN (aus den Formulardaten) zurück.

        Zusätzliche Informationen im Dictionary 'current':
        Pretty_TAN -- formatierte Ausgabe
        Frozen -- zur Steuerung, ob bestimmte Eigenschaften noch änderbar sind.
        Group_OK -- die Gruppen-ID ist vorhanden und gültig
        group_title -- der Gruppentitel
        """
        self.authView()
        res = {'current': None,
               'history': None,
               }
        context = self.context
        request = context.REQUEST
        form = request.form
        # ValueError ggf. abfangen:
        tan = tan2int(form.get('tan'))
        with context.getAdapter('sqlwrapper')() as sql:
            current = None
            query_data = {'tan': tan}
            rows = sql.select('tan', query_data=query_data)
            if not rows:
                return res
            current = rows[0]
            current['Pretty_TAN'] = format_tan(tan)
            current['Frozen'] = current['status'] not in STATUS_USABLE
            ggibi = groupinfo_factory(context, pretty=1, forlist=1)
            group_dict = ggibi(current['group_id'])
            if group_dict:
                current['group_title'] = group_dict['group_title']
                current['Group_OK'] = True
            else:
                current['group_title'] = None
                current['Group_OK'] = False
            key = 'expiration_date'
            val = current[key]
            if val:
                current[key] = val.strftime(DATE_FORMAT)
            res['current'] = current
            res['history'] = sql.select('tan_history_view',
                                        query_data=query_data)
            res['status_values'] = self.tan_statuus(sql)
            res['selectable_groups'] = self.selectable_groups()
        return res

    def _tans_data(self, form=None, pop=0):
        """
        Extrahiere die Felder der tan-Tabelle aus den Formulardaten
        und gib ein dict zurück.

        form -- wenn nicht übergeben, die Formulardaten.

        pop -- wenn True, werden die für die TAN-Generierung relevanten
               Informationen extrahiert, d.h. *entfernt*
        """
        if form is None:
            request = self.context.REQUEST
            form = request.form
        return subdict_ne(form, TAN_FIELDS, pop)

    def _apply_tans_defaults(self, dic):
        """
        Ergänze einige Vorgabewerte
        """
        if 'duration_days' not in dic:
            dic['duration_days'] = 31
        if 'expiration_date' not in dic:
            dic['expiration_date'] = default_expiration_date()
        key = 'additional_info'
        if key in dic:
            dic[key] = dic[key].strip()

    def _check_newtan_data(self, dic):
        """
        Prüfe die Daten für eine neue TAN auf Konsistenz,
        soweit nicht durch Datenbank-Constraints erledigt.
        Nach _apply_tans_defaults anzuwenden.

        Achtung: Das übergebene dic-Objekt wird ggf. modifiziert!
        """
        msglist = []
        if not dic.get('group_id'):
            msglist.append(""'No group given!')
        duration = dic.get('duration_days')
        if duration is not None:
            try:
                val = int(duration)
            except ValueError:
                msglist.append(''"Didn't understand number %(duration)r"
                               " of duration days")
            else:
                if val <= 0:
                    msglist.append(''"Duration period must be"
                                   " at least one day (%(duration)r)")
        expiration_date = dic.get('expiration_date')
        if expiration_date:
            try:
                expiration_date = parse_date(expiration_date)
            except ValueError:
                msglist.append(''"Didn't understand the expiration date"
                               ' %(expiration_date)r')
            else:
                # datetime.date an Datenbank übergeben:
                dic['expiration_date'] = expiration_date
                if expiration_date < date.today():
                    # dieselbe Message-ID wie bei TAN-Einlösung:
                    start = expiration_date
                    msglist.append("Please don't specify dates in the past!"
                                   ' (%(start)s)')
        if dic.get('status') != 'new':
            if not dic.get('additional_info'):
                msglist.append(
                        ""'Status %(status)s requires additional information.')
        quantity = dic.get('quantity')
        if quantity is not None:
            try:
                val = int(quantity)
            except ValueError:
                msglist.append(''"Didn't understand number %(quantity)r"
                               " of TANs to create")
            else:
                if val <= 0:
                    msglist.append(''"Quantity must be "
                                   " at least one (%(quantity)r)")
                max_quantity = 1000
                if val > max_quantity:
                    msglist.append(''"Quantities above %(max_quantity)d "
                                   'are not allowed (%(quantity)r)')
        if msglist:
            _ = make_translator(context)
            for msg in msglist:
                message(context, _(msg) % dic, 'error')
            raise ValueError(""'Please correct your input!')

    def mock_rows(self):
        """
        Gib Beispieldaten zurück, z. B. zum Test von Templates
        """
        self.authManage()
        return [{'tan': 123456789,
                 'quantity': 1,
                 'status': 'new',
                 'group_id': 'group_abc123',
                 'group_title': 'ABC-Gruppe',
                 'duration_days': 31,
                 'owner_id': None,
                 'expiration_date': '2015-04-01',
                 'additional_info': 'Mock-Informationen',
                 'changed_by': 'therp',
                 'last_changed_date': '2014-03-05 16:08:08',
                 'changeset': 65,
                 },
                {'tan': 567891234,
                 'quantity': 1,
                 'status': 'resolved',
                 'group_id': 'group_authors',
                 'group_title': 'Autorengruppe',
                 'duration_days': 365,
                 'owner_id': None,
                 'expiration_date': '2015-04-01',
                 'additional_info': 'Erzeugt für IFAT 2014',
                 'changed_by': 'admin',
                 'last_changed_date': '2014-03-06 13:44:08',
                 'changeset': 66,
                 },
                ]

    def _tan_view_newest(self, sql, query_data=None):
        """
        Gib eine gefilterte und anschließend gruppierte Liste von TANs zurück.
        Die Verknüpfung (Join) wird von der Sicht tan_view geleistet;
        die Ausgabe von tan_view wird gefiltert und anschließend gruppiert.
        """

    def list(self, sql=None):
        """
        Liste die TANs gem. dem gegebenen Filter auf
        """
        context = self.context
        request = context.REQUEST
        form = request.form
        query_data = subdict_ne(form, TAN_FIELDS + ['changeset'])
        if not 'group_id' in query_data:
            try:
                query_data['group_id'] = form['gid']
            except KeyError:
                pass
        if sql is not None:
            return sql.select('tan_view',
                              query_data=query_data)
        with context.getAdapter('sqlwrapper')() as sql:
            return sql.select('tan_view',
                              query_data=query_data)

    def list_redeemable(self, sql=None):
        """
        Liste der TANs, die noch eingelöst werden können
        """
        context = self.context
        request = context.REQUEST
        form = request.form
        form['status'] = STATUS_USABLE
        return self.list(sql)

    def history(self, sql=None):
        """
        Liste die TAN-Historie gem. dem gegebenen Filter auf
        """
        context = self.context
        request = context.REQUEST
        form = request.form
        query_data = subdict_ne(form, TAN_FIELDS)
        if not 'group_id' in query_data:
            query_data.update(subdict_ne(form, ['gid']))
        if sql is not None:
            return sql.select('tan_history_view',
                              query_data=query_data)
        with context.getAdapter('sqlwrapper')() as sql:
            return sql.select('tan_history_view',
                              query_data=query_data)

    def selectable_groups(self):
        """
        Für Auswahlliste:
        Gib die Gruppen zurück, deren Mitglied der angemeldete Benutzer
        ist, oder alle - falls es sich um einen Administrator handelt
        """
        context = self.context
        groupsharing = context.getBrowser('groupsharing')
        if self.can(MANAGE_TANS):
            return groupsharing.get_all_groups()
        else:
            pm = getToolByName(context, 'portal_membership')
            member = pm.getAuthenticatedMember()
            user_id = str(member)
            # derzeit leider nur direkte (explizite) Mitgliedschaften:
            return groupsharing.get_group_memberships(user_id)

    def groups_with_tans(self):
        """
        Zur Auswahl einer Gruppe, für die bereits TANs existieren
        """
        context = self.context
        groupsharing = context.getBrowser('groupsharing')
        ggibi = groupinfo_factory(context, pretty=1, forlist=1)
        if self.can(MANAGE_TANS):
            for dic in self.get_groups_with_tans():
                gid = dic['group_id']
                dic = ggibi(gid)
                if dic:
                    yield dic
        else:
            # dasselbe nochmal, aber mit Filterung nach Mitgliedschaft:
            pm = getToolByName(context, 'portal_membership')
            member = pm.getAuthenticatedMember()
            user_id = str(member)
            is_direct_member_of = is_direct_member__factory(context, user_id)
            for dic in self.get_groups_with_tans():
                gid = dic['group_id']
                if is_direct_member_of(gid):
                    dic = ggibi(gid)
                    if dic:
                        yield ggibi(gid)

    def _get_groups_with_tans(self, sql):
        return sql.query('''
                SELECT DISTINCT group_id
                  FROM tan
                 ORDER BY group_id;
                 ''')

    def get_groups_with_tans(self, sql=None):
        """
        Gib die Tabelle der verwendeten Statuswerte mit der jeweiligen Anzahl zurück
        """
        if sql is not None:
            return self._get_groups_with_tans(sql)
        # with self.context.getAdapter('sqlwrapper')('read only') as sql:
        with self.context.getAdapter('sqlwrapper')() as sql:
            return self._get_groups_with_tans(sql)

    def _export_as_csv(self, fieldnames, table=None,
                       filterfields=None, form=None, sql=None):
        """
        Exportiere einen Auszug aus der tan_view nach csv und gib das
        Ergebnis als String zurück.

        fieldnames -- die Felder (siehe -> tan_view)
        form -- für die SQL-Query
        sql -- optional: der sqlwrapper-Adapter
        """
        context = self.context
        response = context.REQUEST.RESPONSE
        response.setHeader('Content-Type', 'text/csv; charset=utf-8')
        response.setHeader('Content-Disposition',
                           'attachment; filename="tans.csv"')
        if form is None:
            form = context.REQUEST.form
        if filterfields is None:
            filterfields = FREQUENTLY_USED_FILTERS
        query_data = subdict_ne(form, filterfields, pop=0)
        if table is None:
            if 'changeset' in query_data:
                table = 'tan_view_all'
            else:
                table = 'tan_view'
        if sql is None:
            with context.getAdapter('sqlwrapper')() as sql:
                rows = sql.select(table,
                                  fieldnames,
                                  query_data=query_data)
        else:
            rows = sql.select(table,
                              fieldnames,
                              query_data=query_data)
        out = StringIO.StringIO()
        # StringIO.StringIO unterstützt derzeit (Python 2.7.5)
        # leider das Context-Manager-Protokoll (noch?) nicht ...
        ggibi = groupinfo_factory(self.context, pretty=True)
        fieldnames = self.sorted_columns(1, *tuple(fieldnames + ['pretty_title']))
        _ = make_translator(context)  # ggf. auch den Import wieder löschen
        extend = make_key_injector('group_id',
                              ggibi,
                              'pretty_title',
                              _('Unknown group "%(group_id)s"'))
        if 1:  # schonmal eingerückt, für künftiges "with":
            writer = csv_writer(out, dialect='excel_ssv')
            out.write(BOM_UTF8)
            recode = make_safe_stringrecoder(preferred='utf-8')
            writer.writerow(list(map(recode, fieldnames)))
            # Der Writer mag keine dicts!?
            values = make_sequencer(fieldnames, recode)
            for row in rows:
                extend(row)
                writer.writerow(values(row))
            return out.getvalue()

    def get_frequent_filter_names(self):
        """
        Die Namen häufig benutzter Filterfelder
        """
        return FREQUENTLY_USED_FILTERS

    def get_all_fields(self):
        """
        Alle Namen, die bei Bearbeitung benötigt werden
        """
        return self.sorted_columns(*tuple(TAN_FIELDS))

    def csv_export(self):
        """
        Exportiere eine TAN-Liste gemäß den aktuellen Filterkritien
        """
        fieldnames = TAN_FIELDS
        return self._export_as_csv(fieldnames)

    def extract_filters(self, pop=0):
        """
        Extrahiere die üblichen Filter aus dem (dabei standardmäßig nicht
        veränderten) Request
        """
        form = self.context.REQUEST.form
        dic = subdict_ne(form, FREQUENTLY_USED_FILTERS, pop=pop)
        if not 'group_id' in dic:
            dic2 = subdict_ne(form, ['gid'], pop=pop)
            if dic2:
                dic['group_id'] = dic2['gid']
        return dic

    @staticmethod
    def sorted_columns(unique=True, *args):
        """
        Gib die Standardreihenfolge der übergebenen Spalten zurück.

        Bekannte Spalten werden in der konfigurierten Reihenfolge zurückgegeben;
        unbekannte Spalten werden in der angegebenen Reihenfolge angehängt.
        """
        # TODO: durch dict-abgeleitete Klasse ersetzen
        key = frozenset(args)
        try:
            return COLUMNS_SEQUENCE[key]
        except KeyError:
            tail = []
            head = []
            for a in args:
                try:
                    head.append((COLUMNS_ORDER[a], a))
                except KeyError:
                    if unique and a in tail:
                        continue
                    tail.append(a)
            head.sort()
            if unique:
                res = []
                for (sort, a) in head:
                    if not a in res:
                        res.append(a)
            else:
                res = [tup[1] for tup in head]
            res.extend(tail)
            COLUMNS_SEQUENCE[key] = res
            return res

    @log_or_trace(**lot_always)
    def expire(self):
        """
        Deaktiviere abgelaufene TANs.

        Es ist keine Anmeldung erforderlich; es wird lediglich
        exekutiert, was zuvor (mit entsprechender Berechtigung)
        festgelegt wurde.
        """
        buf = []

        def tell(txt):
            msg = '@@tan/expire: %(txt)s' % locals()
            print(msg)
            buf.append(strftime('%F_%T ') + msg)
        context = self.context
        with context.getAdapter('sqlwrapper') as sql:
            expired = sql.query("""
                UPDATE tan
                SET status = 'expired'
                WHERE tan IN (SELECT tan
                              FROM tan_expire_candidates_view)
                RETURNING tan;
                """)
            if expired:
                pm = getToolByName(context, 'portal_membership')
                if pm.isAnonymousUser():
                    user_id = 'system'
                else:
                    member = pm.getAuthenticatedMember()
                    user_id = str(member)
                changeset = self._new_changeset_id(sql, user_id)
                tell('creating changeset %(changeset)s' % locals())
                dic = {'changeset': changeset,
                       'status': 'expired',
                       }
                for row in expired:
                    dic.update(row)
                    sql.insert('tan_history', dic)
                    LOGGER.info('TAN %(tan)s expired', dic)
                msg = '%d TANs expired' % len(expired)
                LOGGER.info(msg)
                tell(msg)
            else:
                msg = 'No TANs found for expiration'
                LOGGER.info(msg)
                if 1:
                    tell(msg)
            return '\n'.join(buf)

    def auth_unitracc_manage_tans(self):

        context = self.context
        if getToolByName(context, 'portal_membership').checkPermission('unitracc: Manage TANs', context):
            return True

        form = context.REQUEST.form

        if form.get('gid'):
            if context.getBrowser('groupdesktop').can_view_group_administration(form.get('gid')):
                return True

        raise Unauthorized

    def tan_example(self):
        """
        Beispielhafter Wert, z. B.  '123.456.789'
        """
        return TAN_EXAMPLE

    def formdata(self):
        """
        Formulardaten; Feldvorbelegungen
        """
        context = self.context
        form = context.REQUEST.form
        date_example = strftime('%d.%m.%Y')
        return {'tan': form.get('tan', ''),
                'tan_example': TAN_EXAMPLE,
                'start': form.get('start', date_example),
                'date_example': date_example,
                }


# vim: ts=8 sts=4 sw=4 si et
