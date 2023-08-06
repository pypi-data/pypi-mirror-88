# -*- coding: utf-8 -*- äöü
# Python compatibility:
from __future__ import absolute_import

# Standard library:
from time import strftime, strptime, time

# Zope:
from AccessControl import Unauthorized
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.cfg import get_raw_config, makeBool
from visaplan.tools.dicts import updated
from visaplan.tools.profile import StopWatch

# Local imports:
from .data import (  # hier aus Gründen der leichteren Testbarkeit:
    DEFAULT_RANGE,
    GLEITENDE_WOCHE,
    GLEITENDER_MONAT,
    GLEITENDES_JAHR,
    GLEITENDES_QUARTAL,
    HEUTE,
    MANUAL_RANGE,
    NAECHSTE_10,
    get_range,
    )
from .utils import (
    calc_range,
    manual_range,
    query_dict,
    range_choices,
    same_day_next_month,
    shortened_query,
    today_00,
    )

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import log_or_trace, pp

logger, debug_active, DEBUG = getLogSupport(defaultFromDevMode=1)
ERROR = logger.error

cfgdict = get_raw_config('event')
if 'profile_active' in cfgdict:
    profile_active = makeBool(cfgdict['profile_active'], False)
else:
    profile_active = debug_active
lot_kwargs = {'logger': logger,
              'debug_level': debug_active,
              }
sw_kwargs = {'enable': bool(profile_active),
             }
del cfgdict, profile_active


class IEventBrowser(Interface):

    def search():
        """ """

    def data(**kwargs):
        """
        Gib ein dict zurück mit Terminen ('brains'), Blätter- ('batch') und
        Formulardaten ('formdata')
        """

    def desktop():
        """
        Gib Termine für den (Gruppen-) Schreibtisch zurück.
        """

    def feed(max_items=10):
        """
        gib Termine fuer den RSS-Feed zurueck
        """

    def searchCurrentEvents():
        """ """

    def format_time():
        """ """


class Browser(BrowserView):

    implements(IEventBrowser)

    @log_or_trace(**lot_kwargs)
    def search(self, **kwargs):
        """
        Allgemeine Suche nach Terminen

        kwargs -- werden abschliessend angewendet
        """
        context = self.context
        form = context.REQUEST.form
        form.update(kwargs)
        pc = getToolByName(context, 'portal_catalog')
        try:
            range = get_range(form)
        except ValueError as e:
            ERROR('invalid range; using default')
            range = DEFAULT_RANGE

        if range == MANUAL_RANGE:
          try:
            start, end = manual_range(form, HEUTE)
          except ValueError as e:
            logger.error(e)
            logger.exception(e)
            if debug_active:
                pp(form)
                from pdb import set_trace; set_trace()
            raise
        else:
            start, end = calc_range(range)

        query = query_dict(start, end,
                           sort_on='start')
        # Event-Typ:
        etype = form.get('category', None)
        if etype:
            query['getCategory'] = etype
            # easyvoc = context.getBrowser('easyvoc')
            # query['getEventType'] = easyvoc.getValue('unitracc-category', etype)
        query.update(kwargs)

        result = pc(query)
        if range == NAECHSTE_10:
            return result[:10]
        return result

    @log_or_trace(**updated(lot_kwargs, trace=0))
    def data(self, **kwargs):
        """
        Gib die Daten für die Kalenderansicht zurück (als dict)

        Dies umfaßt die Daten für das Formular, die ausgegebenen Termine und
        die Auswahl für die Zope-interne Blätterfunktion;
        der Rückgabewert ist ein Dict mit den Schlüsseln:
        - formdata
        - brains
        - batch

        Abgeleitet von --> .search mit der Perspektive, diese Methode zu
        ersetzen.
        """
        context = self.context
        form = context.REQUEST.form
        form.update(kwargs)
        pc = getToolByName(context, 'portal_catalog')
        try:
            range = get_range(form)
        except ValueError as e:
            ERROR('invalid range %(range)r; using default', locals())
            range = DEFAULT_RANGE

        if range == MANUAL_RANGE:
            start, end = manual_range(form, HEUTE)
        else:
            start, end = calc_range(range)

        try:
            batchsize = int(form.get('batchsize', 10))
        except ValueError:
            batchsize = 10

        query = query_dict(start, end,
                           sort_on='start')
        # Event-Typ:
        etype = form.get('category', None)
        if etype:
            query['getCategory'] = etype
            # easyvoc = context.getBrowser('easyvoc')
            # query['getEventType'] = easyvoc.getValue('unitracc-category', etype)
        query.update(kwargs)

        result = pc(query)
        res = {'formdata': {'range': range_choices(range),
                            'category': etype,
                            'batchsize': batchsize,
                            },
               'brains': result,
               }
        if range == NAECHSTE_10:
            result = result[:10]
        batch = context.getBrowser('batch')(result, batchsize)
        res['batch'] = batch
        brains = result
        return res

    def feed(self, max_items=10):
        """
        gib Termine fuer den RSS-Feed zurueck
        (Startpunkt: heute, 0 Uhr)
        """
        now0 = strftime('%Y-%m-%d')
        query = query_dict(DateTime(now0), None,
                           sort_on='start',
                           sort_limit=max_items or None)
        if 0:\
        query = {'review_state': ['inherit', 'published'],
                  'start': {'query': DateTime(now0),
                            'range': 'min'},
                  'sort_limit': max_items,
                  'sort_on': 'start',
                  }
        if debug_active:
            pp(('feed(%(max_items)r):' % locals(),
                query,
                ))
        # wieso hier nochmal prüfen?!
        if max_items is None:
            return self.search(**query)
        else:
            return self.search(**query)[:max_items]

    def desktop(self):
        """
        Gib Termine für den (Gruppen-) Schreibtisch zurück.

        Wenn eine <gid> im Request enthalten ist, werden nur die Termine
        dieser Gruppe (und aller durch sie vermittelten Gruppen)
        zurückgegeben; ansonsten alle Termine des angemeldeten Users und
        aller Gruppen, deren direktes oder indirektes Mitglied er ist.

        TODO:
        Steuerung der Anzahl
        """
        with StopWatch('@@event.desktop',
                       **sw_kwargs
                       ) as stopwatch:
            context = self.context
            pm = getToolByName(context, 'portal_membership')
            if pm.isAnonymousUser():
                raise Unauthorized
            pc = getToolByName(context, 'portal_catalog')
            start = today_00()
            end = same_day_next_month(start, 1)
            query = query_dict(start, end,
                               # sort_limit=2,
                               review_state=None)
            theid = context.REQUEST.form.get('gid')
            if not theid:
                member = pm.getAuthenticatedMember()
                theid = str(member)

            stopwatch.lap('Vorbereitungen')
            userid, group_ids = context.getBrowser('groupsharing'
                                           ).get_user_and_all_groups(theid)
            if userid is None and not group_ids:
                ERROR('desktop: keine Benutzer- oder Gruppeninfo?!'
                      ' %(context)r, %(query)s',
                      locals())
            elif userid is None and len(group_ids) == 1:
                query['groups'] = group_ids.pop()
            elif not group_ids:
                # dann habe ich nur einen User:
                query['author'] = userid
            else:
                # Normalfall: mehrere Gruppen, oder User und mindestens eine
                tmplist = []
                if userid:
                    tmplist.append('author='+userid)
                tmplist.extend(['groups='+gid
                                for gid in sorted(group_ids)])
                query['getCustomSearch'] = {
                        'query': tmplist,
                        'operator': 'or',
                        }
            if debug_active:
                logger.info('desktop() (%r): %s',
                            debug_active,
                            debug_active >= 2
                            and query
                            or  shortened_query(query))
                pp(('@@event.desktop():',
                    shortened_query(query),
                    ))
            stopwatch.lap('query-dict gebaut (%d Gruppen)' % len(group_ids))
            res = pc(query)
            if debug_active:
                logger.info('desktop() --> %d Termine gefunden',
                            len(res))
            return res

    def searchCurrentEvents(self):
        """
        Gets events, which take place between today and the next 30 days. If
        there are more than one events scheduled for each of the days within
        the days range, only the first one of them is picked.
        """
        context = self.context
        pc = getToolByName(context, 'portal_catalog')
        start = today_00()
        end = same_day_next_month(start, 12)
        if 0:
            query = {}
            query['portal_type'] = 'UnitraccEvent'
            query['review_state'] = ['published', 'inherit']
            query['start'] = {'query': (start, end),
                              'range': 'min: max'}
            query['sort_on'] = 'start'
            query["sort_order"] = "ascending"
        query = query_dict(start, end,
                           sort_on='start',
                           sort_order='ascending')
        if debug_active:
            pp(('searchCurrentEvents():',
                query,
                ))

        result = pc(query)

        return result

    def format_time(self, string_):

        try:
            return DateTime(string_).strftime('%d.%m.%Y %H:%M')
        except:
            #No valid datetime
            return ''
# vim: ts=8 sts=4 sw=4 si et hls
