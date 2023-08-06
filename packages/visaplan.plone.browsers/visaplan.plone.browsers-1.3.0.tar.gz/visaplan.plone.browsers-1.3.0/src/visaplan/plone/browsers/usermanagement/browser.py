# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=79
# Python compatibility:
from __future__ import absolute_import

from six import text_type as six_text_type

# Standard library:
from collections import defaultdict
from datetime import date
from hashlib import md5
from json import dumps as json_dumps
from pprint import pformat

# Zope:
import transaction
from AccessControl import Unauthorized
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.base.permissions import (
    ManageCourses,
    ManageGroups,
    ManageUsers,
    ViewGroups,
    )
from visaplan.plone.tools.context import message
from visaplan.plone.tools.forms import back_to_referer
from visaplan.plone.tools.search import normalizeQueryString
from visaplan.tools.classes import ChangeProtected
from visaplan.tools.minifuncs import translate_dummy as _

# Local imports:
from .utils import make_condensed, oneliner, profileBrainInfo, profileInfoDict

try:
    # Local imports:
    from .oldcrumbs import register_crumbs
    register_crumbs()
except ImportError:
    pass

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport

logger, debug_active, DEBUG = getLogSupport(fn=__file__)

try:
    transaction.commit
except NameError:
    raise


class IUserManagement(Interface):

    def search():
        """ """

    def autocomplete_search():
        """
        Benutzersuche, die json-Daten zurückgibt.
        """

    def deleteUser():
        """
        Lösche die im Formular angegebenen Benutzer und Profile
        """

    def lockUsers():
        """
        Sperre die im Formular angegebenen Benutzer
        """

    def unlockUsers():
        """
        Entsperre die im Formular angegebenen Benutzer
        """

    def addUser():
        """
        Erzeuge einen Benutzer (addMember) mit den im Formular angegebenen
        Daten
        """

    def addGroup():
        """
        Erzeuge eine neue Gruppe mit einer automatisch generierten ID
        """

    def download_users():
        """
        Ein Download der Benutzerprofildaten
        """

    def set_group_manager():
        """
        Gruppenadminstrator hinzufügen
        """

    def is_group_manager(group_id=None):
        """
        Ist der angemeldete Benutzer
        der Gruppenleiter der im Request angegebenen Gruppe?
        """

    def remove_group_manager():
        """
        Gruppenadminstrator entfernen
        """

    def canManageUsers():
        """
        Kann der angemeldete Benutzer Benutzer administrieren?
        """

    def authManageUsers():
        """
        Wirft Unauthorized, wenn der angemeldete Benutzer keine Benutzer
        administrieren kann
        """

    def canViewUsers():
        """
        Darf der angemeldete Benutzer Benutzerinformationen sehen?
        """

    def authViewUsers():
        """
        Wirft Unauthorized, wenn der angemeldete Benutzer keine
        Benutzerinformationen sehen darf
        """

    def canManageGroups():
        """
        Kann der angemeldete Benutzer Gruppen administrieren?
        """

    def authManageGroups():
        """
        Wirft Unauthorized, wenn der angemeldete Benutzer keine Gruppen
        administrieren kann
        """

    def canViewGroups():
        """
        Darf der angemeldete Benutzer Gruppeninformationen sehen?
        """

    def authViewGroups():
        """
        Wirft Unauthorized, wenn der angemeldete Benutzer keine
        Gruppeninformationen sehen darf
        """

    def listUsersHavingDuplicateProfiles():
        """
        Liste alle Benutzer auf, denen mehr als ein UnitraccAuthor-Objekt als
        Profil zugeordnet ist
        """

    def deleteProfiles():
        """
        Lösche die im Formular angegebenen Benutzerprofile
        """

    def renameUsers():
        """
        Benenne die angegebenen Benutzerkonten um

        Die Umbenennung von Benutzerkonten ist im Plone-System nicht
        vorgesehen.  Was wirklich passiert, ist:

        - Es wird ein Benutzerobjekt mit der gewünschten neuen ID angelegt.
          Dies kann scheitern (weil die ID schon vergeben ist);
          in diesem Fall wäre hier Schluß.
        - An allen folgenden Stellen wird die alte durch die neue Benutzer-ID
          ersetzt:
          - Gruppenmitgliedschaften
          - Creator-Attribute
          - weitere?
        - Das vorhandene Profil wird dem neuen Benutzerkonto zugeordnet
        - Weitere Übertragung von Eigenschaften?
        - Das alte Benutzerkonto wird gelöscht
        - Wenn das entsprechende Häkchen gesetzt ist, wird eine Mail an die
          konfigurierte Mail-Adresse gesandt.
        """


class Browser(BrowserView):

    implements(IUserManagement)

    def search(self):

        context = self.context

        self.authViewUsers()
        puc = getToolByName(context, 'portal_user_catalog')
        form = context.REQUEST.form

        query = {}

        if form.get('uids'):
            query['UID'] = form.get('uids')

        if form.get('sort_on'):
            query['sort_on'] = form.get('sort_on')

        if form.get('sort_order'):
            query['sort_order'] = form.get('sort_order')

        SearchableText = form.get('SearchableText', '')
        # JQ Autocomplete
        if not SearchableText:
            SearchableText = form.get('term', '')

        if SearchableText:
            # Keine Userwildcard
            queryList = normalizeQueryString(SearchableText)
            query['SearchableText'] = queryList

        if form.get('getLocked', ''):
            query['getLocked'] = form.get('getLocked', '') == 'True' and True or [None, False]

        query['NO_SUBPORTAL'] = 1
        logger.debug('query=%s', pformat(query))

        return puc(**query)

    def autocomplete_search(self):
        """
        Benutzersuche, die json-Daten zurückgibt.
        """
        result = [{"label": six_text_type('%s %s' % (x.getFirstname, x.getLastname)),
                   "value": six_text_type(x.getUserId)
                   }
                  for x in self.search()]

        return json_dumps(result)

    def canManageUsers(self):
        """
        Kann der angemeldete Benutzer Benutzer administrieren?
        """
        return getToolByName(self.context, 'portal_membership').checkPermission(ManageUsers, self.context)

    def authManageUsers(self):
        """
        Wirft Unauthorized, wenn der angemeldete Benutzer keine Benutzer
        administrieren kann
        """
        checkperm = getToolByName(self.context, 'portal_membership').checkPermission
        if not checkperm(ManageUsers, self.context):
            raise Unauthorized

    def canViewUsers(self):
        """
        Darf der angemeldete Benutzer Benutzerinformationen sehen?
        """
        checkperm = getToolByName(self.context, 'portal_membership').checkPermission
        if (checkperm(ManageUsers)
            # es gibt keine Entsprechung zu ViewGroups, oder?
            # *Sehen* dürfen auch Gruppen- und Kurs-Administratoren:
            or checkperm(ManageGroups)
            or checkperm(ManageCourses)
            ):
            return True
        return False

    def authViewUsers(self):
        """
        Wirft Unauthorized, wenn der angemeldete Benutzer keine
        Benutzerinformationen sehen darf
        """
        if not self.canViewUsers():
            raise Unauthorized

    def canManageGroups(self):
        """
        Kann der angemeldete Benutzer Gruppen administrieren?
        """
        return getToolByName(self.context, 'portal_membership').checkPermission(ManageGroups, self.context)

    def authManageGroups(self):
        """
        Wirft Unauthorized, wenn der angemeldete Benutzer keine Gruppen
        administrieren kann
        """
        checkperm = getToolByName(self.context, 'portal_membership').checkPermission
        if not checkperm(ManageGroups, self.context):
            raise Unauthorized

    def canViewGroups(self):
        """
        Darf der angemeldete Benutzer Gruppeninformationen sehen?
        """
        checkperm = getToolByName(self.context, 'portal_membership').checkPermission
        if (checkperm(ViewGroups)
            or checkperm(ManageGroups)
            # *sehen* dürfen auch Benutzer- und Kurs-Administratoren:
            or checkperm(ManageUsers)
            or checkperm(ManageCourses)
            ):
            return True
        return False

    def authViewGroups(self):
        """
        Wirft Unauthorized, wenn der angemeldete Benutzer keine
        Gruppeninformationen sehen darf
        """
        if not self.canViewGroups():
            raise Unauthorized

    def listUsersHavingDuplicateProfiles(self):
        """
        Liste alle Benutzer auf, denen mehr als ein UnitraccAuthor-Objekt als
        Profil zugeordnet ist
        """
        self.authManageUsers()
        context = self.context
        request = context.REQUEST
        form = request.form
        user_id = form.get('user_id') or None
        if user_id is None:
            if context.portal_type == 'UnitraccAuthor':
                user_id = context.getUserId() or None

        return list(self._listUsersHavingDuplicateProfiles(user_id))

    def _listUsersHavingDuplicateProfiles(self, user_id=None):
        query = {}
        if user_id is not None:
            query['getUserId'] = user_id
        # user_id to profiles list:
        u2p = defaultdict(list)

        context = self.context
        puc = getToolByName(context, 'portal_user_catalog')
        for brain in puc(**query):
            u2p[brain.getUserId].append({
                'label': profileBrainInfo(brain),
                'uid': brain.UID,
                })

        for key, vals in u2p.items():
            if (len(vals) >= 2
                or (user_id is not None and key == user_id
                    )):
                yield {'user_id': key,
                       'profiles': vals,
                       }

    def deleteProfiles(self):
        """
        Lösche die im Formular angegebenen Benutzerprofile

        Request-Variablen:

        specs - die Liste der Angaben der zu löschenden Profile:
                {uid}:{max}:{user_id}
        user_id (optional) - nur für die Umleitung zur aufrufenden Seite
        """
        context = self.context
        self.authManageUsers()

        rc = getToolByName(context, 'reference_catalog')
        deleted_profiles = []
        userlog = context.getAdapter('userlog')
        log_profile = userlog.deletedProfile
        request = context.REQUEST
        form = request.form
        # zuerst prüfen, ob nicht etwa *alle*  Profile eines Users zum Löschen
        # angegeben wurden:
        specs = form.get('specs', [])
        given_userid = form.get('user_id') or None
        uids = []
        u2max = ChangeProtected()
        u2uids = defaultdict(list)
        errors = 0
        for spec in specs:
            try:
                uid, max_s, user_id = spec.split(':', 2)
                u2max[user_id] = int(max_s)
                u2uids[user_id].append(uid)
            except:
                errors += 1
                logger.error('deleteProfiles: error in spec %(spec)r', locals())
        if errors:
            message(context,
                    'Error in form data!', 'error')
            return back_to_referer(request, items=[('user_id', given_userid)])

        uids = []
        for user_id, user_uids in u2uids.items():
            cnt = len(user_uids)
            if cnt > u2max[user_id]:
                message(context,
                        "Won't delete all ${cnt} profiles of user ${user_id}!",
                        'error',
                        mapping=locals())
                errors += 1
            uids.extend(user_uids)
        if errors:
            return back_to_referer(request, items=[('user_id', given_userid)])

        for uid in uids:
            po = rc.lookupObject(uid)  # profile object
            if po is None:
                message(context,
                        'Profile ${uid} not found!',
                        'error',
                        mapping=locals())
                continue
            user_id = po.getUserId()
            profile_id = po.getId()
            parent = None
            try:
                po.restrictedTraverse('@@plone_lock_operations'
                                      ).force_unlock(redirect=False)
                parent = po.aq_parent
                res = parent.manage_delObjects(ids=[po.getId()])
                logger.info('manage_delObjects -> %r', res)
                deleted_profiles.append('%(profile_id)r (%(user_id)s)' % locals())
                log_profile(user_id, uid=uid)
            except Exception as e:
                logger.error('Error deleting profile %(profile_id)r'
                             ' (user %(user_id)r, UID %(uid)r)'
                             ' from %(parent)r!',
                             locals())
                logger.exception()
                message(context,
                        'Error deleting profile ${profile_id}'
                        ' for user ${user_id}!',
                        'error',
                        mapping=locals())
        if deleted_profiles:
            message(context,
                    '${cnt} profile(s) deleted: ${info}',
                    mapping={'cnt': len(deleted_profiles),
                             'info': ', '.join(deleted_profiles),
                             })
        elif not uids:
            message(context,
                    'Nothing to do!',
                    'error')
        return back_to_referer(request, items=[('user_id', given_userid)])

    def deleteUser(self):
        """
        Lösche die im Formular angegebenen Benutzer und Profile
        """
        context = self.context
        self.authManageUsers()
        acl = getToolByName(context, 'acl_users')

        form = context.REQUEST.form
        rc = getToolByName(context, 'reference_catalog')
        portal = getToolByName(context, 'portal_url').getPortalObject()
        userlog = context.getAdapter('userlog')
        log_account = userlog.deleted
        log_profile = userlog.deletedProfile
        deleted_users = []
        deleted_profiles = []

        for uid in form.get('uids', []):
            object_ = rc.lookupObject(uid)
            userId = object_.getUserId()
            if form.get('account'):
                if not userId:
                    logger.info('Profil %r: user-ID ist leer', uid)
                elif userId.strip() == 'system':
                    logger.info('Profil %r gehoert User %r!', uid, userId)
                    message(context, _("Won't delete user %(userId)r (owner of profile %(uid)s)!"
                              ) % locals(),
                            'error')
                else:
                    acl.userFolderDelUsers([userId])
                    deleted_users.append(userId)
                    log_account(userId)

            if form.get('profil'):
                object_.restrictedTraverse('@@plone_lock_operations'
                                           ).force_unlock(redirect=False)
                parent = object_.aq_parent
                res = parent.manage_delObjects(ids=[object_.getId()])
                logger.info('manage_delObjects -> %r', res)
                deleted_profiles.append('%(userId)r (%(uid)s)' % locals())
                log_profile(userId, uid=uid)

        if deleted_users:
            message(context, _('%d user(s) deleted: %s'
                      ) % (len(deleted_users),
                           ', '.join(deleted_users),
                           ))
        if deleted_profiles:
            message(context, _('%d profile(s) deleted: %s'
                      ) % (len(deleted_profiles),
                           ', '.join(deleted_profiles),
                           ))
        return context.REQUEST.RESPONSE.redirect(portal.absolute_url() + '/manage_users_view')

    def lockUsers(self):
        """
        Sperre die im Formular angegebenen Benutzer
        """
        return self._toggle_lock(True)

    def _toggle_lock(self, lock):
        """
        Sperre (lock=True) oder entsperre die im Formular angegebenen Benutzer
        """
        context = self.context
        self.authManageUsers()
        rc = getToolByName(context, 'reference_catalog')
        request = context.REQUEST
        form = request.form

        if 0:
            pm = getToolByName(context, 'portal_membership')
            auth_member = pm.getAuthenticatedMember()
            auth_id = str(auth_member)
            auth_fullname = auth_member.getProperty('fullname', auth_id) or auth_id or ''
            tup = (auth_id, auth_fullname)
            admin_info = '%s (%s)' % tup

        def redirect():
            return request.RESPONSE.redirect('/manage_users_view')
        uids = form.get('uids', [])
        if not uids:
            message(context,
                    'Nothing to do!')
            return redirect()

        userlog = context.getAdapter('userlog')
        if lock:
            sing, plu = ('User $info locked',
                         '$cnt users locked: $info',
                         )
            logfunc = userlog.locked
        else:
            sing, plu = ('User $info unlocked',
                         '$cnt users unlocked: $info',
                         )
            logfunc = userlog.unlocked

        changed = []
        condensed = make_condensed(context=context)
        for uid in sorted(set(uids)):
            o = rc.lookupObject(uid)
            if o is None:
                message(context,
                        'User profile $uid not found!',
                        'error',
                        mapping=locals())
                continue

            infodict = profileInfoDict(o)
            o.setLocked(lock)
            o.reindexObject()
            logfunc(**condensed(infodict,
                                **{'uid (profile)': uid}))
            changed.append(oneliner(infodict))

        if changed:
            if not changed[1:]:
                info = changed[0]
                message(context, sing,
                        mapping=locals())
            else:
                info = ', '.join(changed)
                cnt = len(changed)
                message(context, plu,
                        mapping=locals())
        return redirect()

    def unlockUsers(self):
        """
        Entsperre die im Formular angegebenen Benutzer
        """
        return self._toggle_lock(False)

    def addUser(self):
        """
        Erzeuge einen Benutzer (addMember) mit den im Formular angegebenen
        Daten.

        Nur aufgerufen, wenn Benutzer administrativ angelegt -
        für anonyme Registrierung siehe @@registration.set()!
        """
        logger.info('----------- @@usermanagement.addUser aufgerufen! -----------')
        registration = self.context.getBrowser('registration')
        return registration.processNewUser(userid_field='userId',
                                           afterwards='/manage_users_view')

    def renameUsers(self):
        """
        Benenne die angegebenen Benutzerkonten um

        Die Umbenennung von Benutzerkonten ist im Plone-System nicht
        vorgesehen.  Was wirklich passiert, ist:

        - Es wird ein Benutzerobjekt mit der gewünschten neuen ID angelegt.
          Dies kann scheitern (weil die ID schon vergeben ist);
          in diesem Fall wäre hier Schluß.
        - An allen folgenden Stellen wird die alte durch die neue Benutzer-ID
          ersetzt:
          - Gruppenmitgliedschaften
          - Creator-Attribute
          - weitere?
        - Das vorhandene Profil wird dem neuen Benutzerkonto zugeordnet
        - Weitere Übertragung von Eigenschaften?
        - Das alte Benutzerkonto wird gelöscht
        - Wenn das entsprechende Häkchen gesetzt ist, wird eine Mail an die
          konfigurierte Mail-Adresse gesandt.
        """
        return NotImplemented

    def addGroup(self):
        """
        Erzeuge eine neue Gruppe mit einer automatisch generierten ID
        """
        context = self.context

        checkperm = getToolByName(context, 'portal_membership').checkPermission
        if not checkperm(ManageGroups, context):
            raise Unauthorized

        acl = getToolByName(context, 'acl_users')
        form = context.REQUEST.form
        portal = getToolByName(context, 'portal_url').getPortalObject()
        referrer = context.REQUEST.form['referrer']

        if not form.get('title'):
            message(context, _('Please fill all required fields.'), 'error')
            return context.restrictedTraverse('manage_group_add')()

        m = md5()
        m.update(DateTime().strftime('%d.%m.%Y'))
        m.update(form.get('title'))

        group_id = 'group_' + m.hexdigest()
        acl.source_groups.addGroup(group_id, form.get('title'), form.get('description'))

        message(context, _('added group %(group_id)s'
                  ) % locals())

        if referrer == "course":
            return context.REQUEST.RESPONSE.redirect(portal.absolute_url() + '/manage_course_view')
        return context.REQUEST.RESPONSE.redirect(portal.absolute_url() + '/manage_groups_view')

    def download_users(self):
        """
        Ein Download der Benutzerprofildaten
        """
        context = self.context

        self.authManageUsers()
        form = context.REQUEST.form

        # TODO:
        # - echter csv-Download?
        #   (derzeit als application/msexcel deklariertes HTML)
        # - Codierung (safe_encode o.ä.)
        # gf: templates/csv_user_profiles.pt
        string_ = str(context.restrictedTraverse('csv_user_profiles')())

        context.getBrowser('files').download(string_, 'Benutzer.xls', 'xls')

    def reset_date(self):
        """
        setze den Anmeldezeitpunkt für das aktuelle Profil (Kontext) zurück,
        um wieder die Verwendung des Aktivierungs-Links zu ermöglichen

        NOCH NICHT FERTIG!
        """
        context = self.context
        self.authManageUsers()

        if context.portal_type == 'UnitraccAuthor':
            userId = context.getUserId()
            member = context.getBrowser('member')
            member.set(userId)
            user = member.get()
            if user:
                user.setProperty('last_login_time', DateTime('2000/01/01'))
                # context.setProperty('login_time', DateTime('2000/01/01'))
                # context.setLogin_time(DateTime('2000/01/01'))
                context.reindexObject()
                message(context, _('user profile %r reset successfully'
                          ) % (userId,
                               ))
            else:
                message(context, _('member %r not found'
                          ) % (userId,
                               ))
        else:
            message(context, _('This can only be applied to user profiles (%r)'
                      ) % (context.portal_type,
                           ),
                    'error')
        return context.REQUEST.RESPONSE.redirect(portal.absolute_url() + '/manage_users_view')

    def set_group_manager(self):
        """ """
        context = self.context

        checkperm = getToolByName(context, 'portal_membership').checkPermission
        if not checkperm(ManageGroups, context):
            raise Unauthorized

        groupbrowser = context.getBrowser('groups')

        form = context.REQUEST.form
        group = groupbrowser.getById(form.get('group_id'))

        if not form.get('ids'):
            message(context, _('No user selected.'), 'error')
            user_id = None
        else:
            user_id = form.get('ids')[0]

            acl = getToolByName(context, 'acl_users')
            if not acl.getUser(user_id):
                message(context, _('The selected entry is no user.'), 'error')
            else:
                group.set_group_manager(user_id)
                message(context, _('Group manager set.'))

        return context.REQUEST.RESPONSE.redirect(context.REQUEST['HTTP_REFERER'])

    def is_group_manager(self, group_id=None):
        """
        Ist der angemeldete Benutzer
        der Gruppenleiter der im Request angegebenen Gruppe?
        """
        context = self.context
        form = context.REQUEST.form
        if group_id is None:
            group_id = form.get('group_id')
        if not group_id:
            return False
        pm = getToolByName(context, 'portal_membership')
        if pm.isAnonymousUser():
            return False
        groupbrowser = context.getBrowser('groups')
        group = groupbrowser.getById(group_id)
        if not group:
            logger.error('Group %(group_id)r not found', locals())
            return False
        try:
            the_manager = group.get_group_manager()
            user_id = getToolByName(context, 'portal_membership').getAuthenticatedMember.getId()
            return user_id == the_manager
        except AttributeError as e:
            logger.error('Object %(group)r (%(group_id)r) is not a group',
                         locals())
            logger.exception(e)
        return False

    def remove_group_manager(self):
        """ """
        context = self.context

        checkperm = getToolByName(context, 'portal_membership').checkPermission
        if not checkperm(ManageGroups, context):
            raise Unauthorized

        acl = getToolByName(context, 'acl_users')

        groupbrowser = context.getBrowser('groups')

        form = context.REQUEST.form
        group = groupbrowser.getById(form.get('group_id'))
        group.set_group_manager('')
        message(context, _('Group manager removed.'))

        return context.REQUEST.RESPONSE.redirect(context.REQUEST['HTTP_REFERER'])

if 0 and 'Futter fuer den Parser':
    _('added member %(userId)s')
    _("Don't know how to create W3L users")
    _('added member %(userId)s')
    _('added group %(group_id)s')
    _('User %(username)s already exists.')
    _('w3l user %(pseudo)r created')
    _('creation of w3l user %(pseudo)r failed')
