# -*- encoding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et
# Python compatibility:
from __future__ import absolute_import

from six.moves import range

# Zope:
from DateTime import DateTime
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.cfg import get_debug_active
from visaplan.plone.tools.context import getbrain, make_translator, message
from visaplan.plone.tools.search import normalizeQueryString
from visaplan.plone.unitracctool.unitraccfeature.utils import MEMBERSFOLDER_UID

# Local imports:
from .utils import (
    get_formatted_name,
    get_title_and_name,
    joinNonemptyAttributes,
    make_getter,
    )

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport

logger, debug_active, DEBUG = getLogSupport()

if 0 and 'nur fuer den Parser':
    _('Login failed. Your account is locked.'
      ' Please contact the support team.')
    _('Login failed. Your account is locked.'
      ' Please use the activation link'
      ' in the mail we sent to you,'
      ' or contact the support team.')

DEFAULT, MINIMAL, SMALL, MEDIUM, LARGE = list(range(5))
COMPLETE = 999
CARDLEVEL = {'minimal': MINIMAL,
             'small': SMALL,
             'medium': MEDIUM,
             'large': LARGE,
             'complete': COMPLETE,
             }
LEVELNAME = {}
for key, val in CARDLEVEL.items():
    LEVELNAME[val] = key
# Aliase:
CARDLEVEL['short'] = SMALL


class IAuthorBrowser(Interface):

    def getRelated():
        """Return related contact of context if exists"""

    def search():
        """ """

    def getImage():
        """ """

    def getImageLarge():
        """ """

    def create():
        """ """

    def getAuthor(uid):
        """ """

    def getAuthorInfo(uid):
        """
        gib eine Zeichenkette mit Autoreninformationen zurück
        """

    def getByUserId(userId):
        """
        Gib das Profil des Benutzers der übergebenen ID zurück
        """

    def getBrainByUserId(userId):
        """ """

    def checkLocked():
        """ """

    def get():
        """ """

    def get_formatted_name(brain):
        """ """

    def searchProfiles(query, b_start):
        """ """

    def getLargeBusinessCard(uid):
        """ """

    def getShortListEntry(brain):
        """
        Gib sehr knappe Informationen zurück,
        gerade ausreichend für eine Link-Liste
        """

    def getMediumBusinessCard(uid):
        """ """

    def getSmallBusinessCard(uid):
        """ """

    def getMinimalBusinessCard(uid):
        """ """

    def getCardsByGroupId(groupId):
        """
        Hole alle Gruppenmitglieder und bilde dafür die Visitenkarten
        """

    def getShortListEntryByUserId(user_id):
        """ """


class Browser(BrowserView):

    implements(IAuthorBrowser)

    UID = MEMBERSFOLDER_UID    # /management/autoren

    def __init__(self, context, request):
        """ """
        BrowserView.__init__(self, context, request)
        # wird das in Templates noch gebraucht,
        # oder kann das (i.e., die ganze __init__-Methode) weg?!
        self.pc = getToolByName(context, 'portal_catalog')

    def getByUserId(self, userId):
        """
        Gib das Profil des Benutzers der übergebenen ID zurück

        Die Eigenschaft "Creator" verknüpft das Profil mit dem Zope-Benutzer
        """
        context = self.context
        puc = getToolByName(context, 'portal_user_catalog')

        query = {
            'portal_type': 'UnitraccAuthor',
            'Creator': userId,
            }

        brains = puc(query)

        if len(brains) == 1:
            return brains[0].getObject()

    def getBrainByUserId(self, userId):
        context = self.context
        puc = getToolByName(context, 'portal_user_catalog')

        query = {
            'portal_type': 'UnitraccAuthor',
            'getUserId': userId,
            }
        brains = puc(query)

        if len(brains) == 1:
            return brains[0]

    def get(self, userId=''):
        context = self.context
        puc = getToolByName(context, 'portal_user_catalog')
        if not userId:
            userId = context.getBrowser('member').getId()

        query = {}
        query['portal_type'] = 'UnitraccAuthor'
        query['getUserId'] = userId

        brains = puc(query)

        if len(brains) == 1:
            return brains[0].getObject()

    def create(self):
        """ """
        context = self.context

        pm = getToolByName(context, 'portal_membership')
        if not pm.isAnonymousUser():
            puc = getToolByName(context, 'portal_user_catalog')
            userId = context.getBrowser('member').getId()
            portal = getToolByName(context, 'portal_url').getPortalObject()
            sm = portal.getAdapter('securitymanager')
            sm(userId='system')
            sm.setNew()

            query = {}
            query['portal_type'] = 'UnitraccAuthor'
            query['Creator'] = userId

            brains = puc(query)

            if not brains:
                rc = getToolByName(context, 'reference_catalog')
                folder = rc.lookupObject(self.UID)
                if folder:
                    createObject = folder.getAdapter('createobject')
                    object_ = createObject('UnitraccAuthor')

                    object_.setUserId(userId)
                    changeowner = object_.getBrowser('changeowner')
                    changeowner.set(userId)
                    object_.reindexObject()
            else:
                for brain in brains:
                    object_ = brain._unrestrictedGetObject()
                    object_.reindexObject(idxs=['getLastLogin'])
            sm.setOld()

    def getRelated(self, uid):
        context = self.context
        rc = getToolByName(context, 'reference_catalog')

        query = {}
        query['relationship'] = 'creators'
        query['sourceUID'] = uid

        list_ = []
        for uid in [brain.targetUID for brain in rc(query)]:
            brain = getbrain(context, uid)
            if brain:
                list_.append(brain)

        return list_

    def getAuthor(self, uid):
        brains = self.getRelated(uid)
        if brains:
            return brains[0]

    def getAuthorInfo(self, uid):
        """
        gib eine Zeichenkette mit Autoreninformationen zurück
        (oder None)
        """
        # siehe auch visaplan.plone.tools.brains.make_collector
        brains = self.getRelated(uid)
        if brains:
            return get_title_and_name(brains[0])

    def search(self):
        """ """
        context = self.context
        form = context.REQUEST.form
        puc = getToolByName(context, 'portal_user_catalog')
        txng = context.getBrowser('txng')

        query = {}

        queryString = form.get('SearchableText', '')
        DEBUG('search: queryString (1) = %(queryString)r', locals())
        queryString = txng.processWords(queryString).strip()
        DEBUG('search: queryString (2.txng) = %(queryString)r', locals())

        if queryString:
            queryString = '*' + queryString + '*'
            query['SearchableText'] = queryString

        query['portal_type'] = 'UnitraccAuthor'
        if context.UID() != MEMBERSFOLDER_UID:  # Benutzerverwaltung
            query['getExcludeFromNav'] = False

        return puc(query)

    def getImage(self):
        """ """
        try:
            context = self.context
            scaling = context.getBrowser('scaling')
            data = scaling.get()
            if data:
                return data
            scale = context.REQUEST.form.get('scaling')
            trave = context.restrictedTraverse
            if scale and scale in ["60x80", "120x160", "180x240"]:
                return trave('dummy_author_' + scale + '.png')._data

            return trave('dummy_author.png')._data
        except Exception as e:
            logger.error('%(context)r->getImage(%(scale)r):', locals())
            logger.exception(e)

    def getImageLarge(self):
        """ """
        context = self.context
        scaling = context.getBrowser('scaling')
        data = scaling.get()
        if data:
            return data
        return context.restrictedTraverse('dummy_author_large.png')._data

    def checkLocked(self):
        """
        Ist der aktuell "angemeldete" Benutzer (bzw. sein Profil) gesperrt?
        """
        context = self.context

        portal = getToolByName(context, 'portal_url').getPortalObject()
        pm = getToolByName(portal, 'portal_membership')
        if not pm.checkPermission(ManagePortal, portal):
            member = pm.getAuthenticatedMember()
            userId = member.getId()
            author = context.getBrowser('author').getByUserId(userId)

            if author and author.getLocked():
                last_login = author.getLastLogin()
                if last_login == DateTime('2000/01/01'):
                    messagecontent = ('Login failed. Your account is locked.'
                                      ' Please use the activation link'
                                      ' in the mail we sent to you,'
                                      ' or contact the support team.')
                else:
                    messagecontent = ('Login failed. Your account is locked.'
                                      ' Please contact the support team.')

                message(context, messagecontent)
                pm.logoutUser(REQUEST=context.REQUEST)
                return True

    def get_title_and_name(self, brain):
        """
        Gib Titel, Vor- und Nachnamen zurück
        """
        return get_title_and_name(brain)

    def get_formatted_name(self, brain):
        """
        Gib Vor- und Nachnamen zurück
        """
        return get_formatted_name(brain)

    def searchProfiles(self, query, b_start):
        """ Suche vorhandene Nutzerprofile und gib das Ergebnis
            als JSON-Objekt zurück.
        """

        context = self.context
        puc = getToolByName(context, 'portal_user_catalog')
        pcquery = {}
        amount = 20
        # Bilde die Abfrage
        # excludeFromNav == False --> Visitenkarte anzeigen:
        pcquery['getExcludeFromNav'] = False
        # gesperrte Benutzer nicht auflisten:
        pcquery['getLocked'] = False
        pcquery['sort_on'] = 'getLastnameIndex'
        SearchableText = query.strip()
        if SearchableText:
            queryList = normalizeQueryString(SearchableText)
            if queryList:
                pcquery['SearchableText'] = queryList

        # -*- Hole Ergebnis
        DEBUG(pcquery)
        queryResult = puc(pcquery)

        result = [author for author in queryResult
                  if author['getUserId']]
        b_start = int(b_start)
        return {'result': result[b_start: amount + b_start],
                'pagination': result}

    @staticmethod
    def joinNonemptyAttributes(dic, *attributes, **kwargs):
        """
        Gib eine Zeichenkette zurück, die aus den nicht-leeren
        Attributen des übergebenen dict-Werts gebildet wird.

        dic -- das Dictionary (z.B. aus self.getBrainByUserId)
        separator -- wenn nicht None, der zur Verkettung verwendete
                     String

        unbenannte Argumente: jeweils ein String (Attributname), oder
        ein 2-Tupel aus dem Attributnamen und einer Funktion zur
        Transformation.
        """
        return joinNonemptyAttributes(dic, *attributes, **kwargs)

    def getBusinessCard(self, userId, size=DEFAULT, brain=None):
        """
        Gib die Daten für eine Visitenkarte der angegebenen Größe zurück.
        """
        if not isinstance(size, int):
            size = CARDLEVEL[size]
        assert size >= 0
        if not size:
            size = MEDIUM
        if brain is None:
            brain = self.getBrainByUserId(userId)
        if not brain:
            logger.warning("Doppeltes Profil gefunden fuer userID: %s", userId)
            return brain
        context = self.context
        result = {}

        # minimal:
        voc = context.getBrowser('easyvoc').get('unitracc-form-of-address')
        _ = make_translator(context)

        def transformPrefix(nr):
            return _(voc[int(nr) - 1][1])

        result['name'] = joinNonemptyAttributes(brain,
                                                ('getFormOfAddress', transformPrefix),
                                                'getAcademicTitle',
                                                'getFirstname',
                                                'getLastname',
                                                )
        result['image'] = brain.getURL()
        result['user'] = brain.UID
        if size < SMALL:
            return result
        get = make_getter(brain)
        # small/short:
        result['company'] = get('getBusinessCompany')
        result['depart'] = get('getBusinessDepartment')
        result['position'] = get('getBusinessPosition')
        if size < MEDIUM:
            return result

        # medium:
        result['email'] = get('getBusinessEmail')
        result['phone'] = get('getBusinessPhone')
        result['fax'] = get('getBusinessFax')
        if size < LARGE:
            return result

        # large:
        result['city'] = joinNonemptyAttributes(brain,
                                                'getBusinessZip',
                                                'getBusinessCity',
                                                )
        result['street'] = get('getBusinessStreet')

        url = get('getBusinessWeblink')
        result['web'] = (url != 'http://') and url or ''

        country = get('getBusinessCountry')
        if country:
            countrylist = context.getBrowser('voccountry')
            result['country'] = countrylist.get_country_for_code(country)
        else:
            result['country'] = ''

        if 'getCode' in brain:
            codes = brain['getCode']
            logger.info('getBusinessCard: getCode = %(codes)r', locals())
        else:
            logger.error('getBusinessCard: getCode nicht vorhanden')
            codes = None
        if codes and isinstance(codes, (list, tuple)):
            codelist = context.getBrowser('industrialsector')
            try:
                liz = [nonempty
                       for nonempty in [codelist.getValue(code)
                                        for code in codes
                                        if code]
                       if nonempty]
                codes = ', '.join(liz)
            except AttributeError as e:
                logger.error('Can\'t evaluate codes for user %r', userId)
                logger.exception(e)
        result['code'] = codes

        return result

    def getMinimalBusinessCard(self, userId):
        """ get smallest version of Business card (image and name) """
        return self.getBusinessCard(userId, MINIMAL)

    def getShortBusinessCard(self, userId, author=None):
        """ return short version of the Business Card as dict"""
        return self.getBusinessCard(userId, SMALL, author)

    def getShortListEntryByUserId(self, user_id):
        # für Python-Ausdruck in pt auch ohne Docstring verfügbar
        try:
            brain = self.getBrainByUserId(user_id)
            if brain:
                return self.getShortListEntry(brain)
        except Exception as e:
            logger.error('getShortListEntryByUserId(%(user_id)r):', locals())
            logger.exception(e)

    def getShortListEntry(self, brain):
        """
        Gib sehr knappe Informationen zurück,
        gerade ausreichend für eine Link-Liste
        """
        try:
            profile = {'name': self.get_title_and_name(brain),
                       'id': brain.getUserId,
                       'email': brain.getEmail,
                       'path': brain.getPath(),
                       # auch möglich: '/resolveUID/%s' % brain.UID
                       }
        except AttributeError as e:
            logger.error('getShortListEntry(brain=%(brain)r):', locals())
            logger.exception(e)
            try:
                logger.error('dict(brain) = %r', dict(brain))
            except Exception:
                logger.error('(dict(brain) leider nicht verfuegbar)')
            raise
        return profile

    def getSmallBusinessCard(self, userId, brain=None):
        return self.getBusinessCard(userId, SMALL, brain)

    def getMediumBusinessCard(self, userId):
        """ get medium version of BusinessCard """
        return self.getBusinessCard(userId, MEDIUM)

    def getLargeBusinessCard(self, userID, brain=None):
        """ Get the complete Business Card """
        return self.getBusinessCard(userID, LARGE, brain)

    def getCardsByGroupId(self, groupId):
        """
        Hole alle Gruppenmitglieder und bilde dafür die Visitenkarten
        """
        context = self.context
        groupBrowser = context.getBrowser('groups')
        group = groupBrowser.getById(groupId)
        result = []
        if group is not None:
            members = group.getMemberIds()
            for memberid in members:
                try:
                    pass
                except:
                    # Gruppenverschachtelung
                    # Nur direkte Mitglieder haben Zugriff.
                    continue
        return result
