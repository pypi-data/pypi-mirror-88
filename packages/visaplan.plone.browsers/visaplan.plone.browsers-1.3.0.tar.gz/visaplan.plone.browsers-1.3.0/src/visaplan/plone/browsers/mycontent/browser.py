# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et tw=72 hls
# Python compatibility:
from __future__ import absolute_import

from six import string_types as six_string_types

# Zope:
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.groups.unitraccgroups.utils import split_group_id
from visaplan.plone.tools.context import getbrain
from visaplan.tools.minifuncs import check_kwargs

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import log_or_trace, pp

logger, debug_active, DEBUG = getLogSupport()
lot_kwargs = {# 'trace': True,
              }

# Standard library:
from pprint import pformat

# ------------------------------------------------------ [ Daten ... [
UIDCHARS = set('abcdef0123456789')
BLACKLIST_UIDS = ('e8dfc4253bc0ad402d48dc862d20821c',  # Mediathek
                  '1255c69f5497ffb66ab21dfb9108ec4e',  # Vorträge
                  )
# ------------------------------------------------------ ] ... Daten ]

def as_list(seq, writable=False):
    """
    Gib die übergebene Sequenz als Liste zurück, um sie mehrfach
    auslesen zu können (Iteratoren "verbrauchen" sich beim ersten
    Lesen);
    wenn das Ergebnis schreibbar sein soll, writable=True übergeben.

    Bislang berücksichtigt: Listen, Tupel, Iteratoren
    """
    if isinstance(seq, list):
        return seq
    elif isinstance(seq, tuple):
        if writable:
            return list(seq)
        return seq
    else:
        return list(seq)


class IMyContent(Interface):

    def getCount(getCustomSearch):
        """ """

    def getByType(getCustomSearch):
        """ """

    def get(getCustomSearch, **kwargs):
        """
        Abgeleitet von getByType;
        die Filterkriterien in getCustomSearch werden jedoch nicht
        automatisch ergaenzt.
        """

    def getForGroup(gid, getCustomSearch):
        """
        (VERMUTLICH OBSOLET)

        Abgeleitet von getByType fuer die Suche nach Gruppen
        """

    def getCollaborations():
        """
        gib alle Strukturelemente zurueck, deren Autorengruppe der
        angemeldete Benutzer angehoert
        """

    def getReadableStructures():
        """
        gib alle Strukturelemente zurueck, deren Lesergruppe der
        angemeldete Benutzer angehoert
        """

    def getBothLists():
        """
        gib sowohl die bearbeitbaren als auch die lesbaren
        Strukturelemente zurueck

        (vereinigt getCollaborations und getReadableStructures)
        """

    def getOneList(**kwargs):
        """
        Gib ein dict-Objekt zurück mit folgenden Schlüsseln:
        - thelist -- eine Liste mit allen Autoren- und Lesergruppen,
                     denen der angemeldete Beutzer (ggf. gefiltert nach
                     einer vermittelnde Gruppe) angehört
        - has_collab -- enthält die Liste Autorengruppen?
        - has_watched -- enthält die Liste Lesergruppen?

        Jedes Element kommt nur einmal vor - die Autorengruppe
        berechtigen schließlich auch zur Ansicht.

        Basiert auf getBothLists.
        """


class Browser(BrowserView):

    implements(IMyContent)

    def getByType(self, getCustomSearch):
        """
        Der Typ wird im Argument getCustomSearch als Suchausdruck
        uebergeben; der Besitzer ("author") wird als UND-verknuepfte
        weitere Bedingung automatisch hinzugefuegt
        """
        context = self.getContext()

        pm = getToolByName(context, 'portal_membership')
        if pm.isAnonymousUser():
            raise Unauthorized

        pc = getToolByName(context, 'portal_catalog')
        member = getToolByName(context, 'portal_membership').getAuthenticatedMember()
        if isinstance(getCustomSearch, six_string_types):
            getCustomSearch = [getCustomSearch]
        elif isinstance(getCustomSearch, tuple):
            getCustomSearch = list(getCustomSearch)

        getCustomSearch.append('author=' + member.getId())

        query = {}
        query['getCustomSearch'] = {'query': getCustomSearch,
                                    'operator': 'and'}
        query['sort_on'] = 'getEffectiveIndex'
        query['sort_order'] = 'reverse'
        query['review_state'] = ['accepted', 'private', 'submitted',
                                 ]
        if debug_active:
            DEBUG('getByType, query: \n%s', pformat(query))
        return pc(query)

    def get(self, getCustomSearch, **kwargs):
        """
        Abgeleitet von getByType;
        die Filterkriterien in getCustomSearch werden jedoch nicht
        automatisch ergaenzt.

        Alle query-Argumente außer getCustomSearch können durch
        Schlüsselwortargumente übersteuert werden
        (siehe search_kwargs, our-articles.pt).
        """
        context = self.context
        pm = getToolByName(context, 'portal_membership')
        if pm.isAnonymousUser():
            raise Unauthorized

        if isinstance(getCustomSearch, six_string_types):
            getCustomSearch = [getCustomSearch]
        elif isinstance(getCustomSearch, tuple):
            getCustomSearch = list(getCustomSearch)
        try:
            doprint = getCustomSearch[0].endswith('UnitraccEvent')
        except (IndexError, Exception):
            doprint = False

        query = {'getCustomSearch': {'query': getCustomSearch,
                                     'operator': 'and'},
                 'sort_on': 'getEffectiveIndex',
                 'sort_order': 'reverse',  # reverse == descending
                 'review_state': ['accepted', 'private', 'submitted',
                                  ],
                 'NO_SUBPORTAL': True,
                 }
        if doprint and debug_active:
            pp([('getCustomSearch:', getCustomSearch),
                ('kwargs:', kwargs),
                ('query:', query),
                ])
        if kwargs:
            refine = dict(kwargs)
            if 'getCustomSearch' in refine:
                del refine['getCustomSearch']
            query.update(refine)
            if doprint and debug_active:
                pp(['... modifiziert anhand kwargs:',
                    ('query:', query),
                    ])

        pc = getToolByName(context, 'portal_catalog')
        if debug_active:
            DEBUG('get, query: \n%s', pformat(query))
        return pc(query)

    def getForGroup(self, gid, getCustomSearch):
        """
        Abgeleitet von getByType fuer die Suche nach Gruppen
        """
        context = self.context

        pm = getToolByName(context, 'portal_membership')
        if pm.isAnonymousUser():
            raise Unauthorized

        pc = getToolByName(context, 'portal_catalog')
        if isinstance(getCustomSearch, six_string_types):
            getCustomSearch = [getCustomSearch]
        elif isinstance(getCustomSearch, tuple):
            getCustomSearch = list(getCustomSearch)

        getCustomSearch.append('author=' + gid)

        query = {}
        query['getCustomSearch'] = {'query': getCustomSearch,
                                    'operator': 'and'}
        query['sort_on'] = 'getEffectiveIndex'
        query['sort_order'] = 'reverse'
        if debug_active:
            DEBUG('getForGroup, query: \n%s', pformat(query))
        rslt = pc(query)
        return rslt

        return pc(query)

    def getCount(self, getCustomSearch):
        """ """
        return len(self.getByType(getCustomSearch))

    @staticmethod
    def isAuthorGroupID(groupId):
        """
        folgt die Gruppen-ID der Konvention fuer eine Autorengruppe?

        Zwischen Praefix und Suffix steht eine UID, die keinen weiteren
        Unterstrich enthaelt
        """
        return split_group_id(groupId)['role'] == 'Author'

    @staticmethod
    def isReaderGroupID(groupId):
        """
        folgt die Gruppen-ID der Konvention fuer eine Lesergruppe?
        """
        return split_group_id(groupId)['role'] == 'Reader'

    @staticmethod
    def looksLikeAUID(uid):
        """
        Sieht der übergebene String wie eine UID aus?
        """
        if len(uid) != 32:
            return False
        return set(uid).issubset(UIDCHARS)

    @staticmethod
    def isGenericGroupID(groupId, suffix):
        """
        folgt die Gruppen-ID der Konvention fuer eine generische Gruppe
        mit <suffix>-Rolle?
        """
        dic = split_group_id(groupId)
        return dic['role'] == suffix

    def getBlacklist(self):
        """
        Ausschlussliste fuer Zusammenarbeitsobjekte
        """
        return BLACKLIST_UIDS

    def _defaultQuery(self):
        return {'sort_on': 'getTitleIndex',
                'UID': [],
                'Language': 'all',
                'NO_SUBPORTAL': True,
                }

    def getCollaborations(self):
        """
        gib alle Strukturelemente zurueck, deren Autorengruppe der
        angemeldete Benutzer angehoert.

        Die Lesergruppen werden hier nicht mit eingeschlossen, weil sie
        separat behandelt werden.
        """
        context = self.context
        acl = getToolByName(context, 'acl_users')
        member = getToolByName(context, 'portal_membership').getAuthenticatedMember()
        pc = getToolByName(context, 'portal_catalog')
        query = self._defaultQuery()
        blacklist = self.getBlacklist()

        for groupId in member.getGroups():
            if self.isAuthorGroupID(groupId):   # nur ..._Author
                prefix, uid, role = groupId.split('_')
                if uid not in blacklist:
                    query['UID'].append(uid)

        liz = []
        first = 0
        sm = context.getAdapter('securitymanager')
        try:
            sm(userId='system')
            sm.setNew()
            return pc(query)
        finally:
            try:
                sm.setOld()
            except AttributeError as e:
                logger.warn('getCollaborations(): %s' % str(e))

    def getReadableStructures(self):
        """
        gib alle Strukturelemente zurueck, deren Lesergruppe der
        angemeldete Benutzer angehoert.

        Die Autorengruppen werden hier nicht mit eingeschlossen, weil
        sie separat behandelt werden ("Zusammenarbeit")
        """
        context = self.context
        acl = getToolByName(context, 'acl_users')
        member = getToolByName(context, 'portal_membership').getAuthenticatedMember()
        pc = getToolByName(context, 'portal_catalog')
        query = self._defaultQuery()
        blacklist = self.getBlacklist()

        for groupId in member.getGroups():
            if not self.isReaderGroupID(groupId):   # nur _Reader
                continue
            prefix, uid, role = groupId.split('_')
            if uid in blacklist:
                continue
            brain = getbrain(context, uid)
            if brain is None:
                logger.warn('Kein Objekt zur Reader-Gruppe (uid=%s)'
                            % uid)
                continue
            # Bei Lesergruppen vorerst keinerlei Filterung nach Status:
            query['UID'].append(uid)

        # wenn nicht als 'system' ausgeführt, fehlen anschließend
        # bestimmte Objekte in der Liste; siehe UNITRACC-320
        sm = context.getAdapter('securitymanager')
        try:
            sm(userId='system')
            sm.setNew()
            return pc(query)
        finally:
            try:
                sm.setOld()
            except AttributeError as e:
                logger.warn('getReadableStructures(): %s' % str(e))

    @log_or_trace(debug_active, **lot_kwargs)
    def getBothLists(self, forgroup=None, recurse=False):
        """
        gib sowohl die bearbeitbaren als auch die lesbaren
        Strukturelemente zurueck

        (vereinigt getCollaborations und getReadableStructures)
        """
        context = self.context
        acl = getToolByName(context, 'acl_users')
        pc = getToolByName(context, 'portal_catalog')
        groupsharing = context.getBrowser('groupsharing')
        query_a = self._defaultQuery()
        # dict(query_a) wäre nicht gut genug:
        query_r = self._defaultQuery()

        if forgroup is None:
            member = getToolByName(context, 'portal_membership').getAuthenticatedMember()
            groups = member.getGroups()
            if recurse and groups:
                groupset = set(groups)
                add = groupset.add
                gigmbgi = groupsharing.get_inherited_group_memberships_by_group_id
                for group in groups:
                    for newgroup in gigmbgi(group):
                        add(newgroup['id'])
                groups = list(groupset)
        else:
            # FIXME: Funktioniert bisher nur für "echte" Autoren- und
            #        Lesergruppen
            # TODO: Alle durch diese Gruppe vermittelten
            #       Mitgliedschaften ermitteln
            all_groups = groupsharing.get_inherited_group_memberships_by_group_id(forgroup)
            groups = [x['id'] for x in all_groups]
            groups.append(forgroup)

        blacklist = self.getBlacklist()
        if debug_active:
            DEBUG('blacklist: %s', blacklist)

        groupdicts = [split_group_id(groupId)
                      for groupId in groups
                      ]
        # Gruppen ohne Rolle sind für diese Listen irrelevant:
        groupdicts = [dic
                      for dic in groupdicts
                      if dic['uid'] is not None
                         and dic['uid'] not in blacklist
                      ]

        authorgroup_uids = set([dic['uid']
                                for dic in groupdicts
                                if dic['role'] == 'Author'
                                ])
        if authorgroup_uids:
            query_a['UID'].extend(authorgroup_uids)

            def get_writeable():
                if debug_active:
                    DEBUG('get_writeable: query_a=%s', query_a)
                return pc(query_a)
        else:
            def get_writeable():
                return []

        # Wenn Author, ist Reader uninteressant (Dopplungen vermeiden):
        readergroup_uids = set([dic['uid']
                                for dic in groupdicts
                                if dic['role'] == 'Reader'
                                and dic['uid'] not in authorgroup_uids
                                ])
        if readergroup_uids:
            query_r['UID'].extend(readergroup_uids)

            def get_readable():
                if debug_active:
                    DEBUG('get_readable: query_r=%s', query_r)
                return pc(query_r)
        else:
            def get_readable():
                return []

        # wenn nicht als 'system' ausgeführt, fehlen anschließend
        # bestimmte Objekte in der Liste; siehe UNITRACC-320
        sm = context.getAdapter('securitymanager')
        try:
            sm(userId='system')
            sm.setNew()
            return get_writeable(), get_readable()
            # return pc(query_a), pc(query_r)
        finally:
            try:
                sm.setOld()
            except AttributeError as e:
                logger.warn('getBothLists(): %s' % str(e))

    def getOneList(self, **kwargs):
        """
        Gib ein dict-Objekt zurück mit folgenden Schlüsseln:
        - thelist -- eine Liste mit allen Autoren- und Lesergruppen,
                     denen der angemeldete Beutzer (ggf. gefiltert nach
                     einer vermittelnde Gruppe) angehört
        - has_collab -- enthält die Liste Autorengruppen?
        - has_watched -- enthält die Liste Lesergruppen?

        Jedes Element kommt nur einmal vor - die Autorengruppe
        berechtigen schließlich auch zur Ansicht.
        """
        forgroup = kwargs.pop('forgroup', None)
        recurse = kwargs.pop('recurse', None)
        check_kwargs(kwargs)  # raises TypeError if necessary
        writable, readable = self.getBothLists(forgroup, recurse)
        writable = as_list(writable)
        readable = as_list(readable)
        return {'thelist': [{'brain': x,
                             'writable': True,
                             }
                            for x in writable] +
                           [{'brain': x,
                             'writable': False,
                             }
                            for x in readable],
                'has_collab': bool(writable),
                'has_watched': bool(readable),
                }
