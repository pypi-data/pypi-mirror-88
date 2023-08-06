# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et tw=79
# Python compatibility:
from __future__ import absolute_import

from six import string_types as six_string_types

# Standard library:
from time import strftime

# Zope:
import transaction
from AccessControl import Unauthorized
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.MailHost.MailHost import MailHostError
from zExceptions import Redirect
from ZODB.POSException import ReadOnlyError

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.browsers.password.browser import InvalidPassword
from visaplan.plone.browsers.tan.utils import check_tan
from visaplan.plone.tools.context import (
    getActiveLanguage,
    make_translator,
    message,
    )
from visaplan.plone.tools.forms import back_to_referer
from visaplan.plone.unitracctool.unitraccfeature.utils import MEMBERSFOLDER_UID
from visaplan.tools.dicts import subdict
from visaplan.tools.http import make_url

# Local imports:
from .interface import IRegistrationBrowser
from .utils import (
    get_hostname,
    get_ip,
    makeActivationLink,
    no_password_fieldname,
    )

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import log_or_trace, pp

logger, debug_active, DEBUG = getLogSupport(fn=__file__)

lot_kwargs = {'logger': logger,
              'trace': debug_active > 1,
              'verbose': True,
              }

try:
    transaction.savepoint
except NameError:
    raise

LANGUAGES = ['de', 'en', 'es', 'fr']


### [ Exception-Klassen für Benutzernamen-Überprüfung ... [
class InvalidUsername(ValueError):
    msgmask = ""'Invalid username %(username)r'
    # obiger String wird derzeit vom Parser nicht gefunden (!); Workaround:
    if 0 and 'Futter fuer den Generator':
        _('Invalid username %(username)r')

    def mkmsg(self, translate, **kwargs):
        self.msg = translate(self.msgmask) % kwargs

    def __str__(self):
        return self.msg

    def __init__(self, translate, username):
        self.username = username
        self.mkmsg(translate, username=username)


class EmptyUsername(InvalidUsername):
    msgmask = ""'Empty username not allowed (%(username)r)'
    if 0 and 'Futter fuer den Generator':
        _('Empty username not allowed (%(username)r)')


class InvalidChars(InvalidUsername):
    msgmask = ""'Invalid username %(username)r: ' \
                'character %(ch)r not allowed'
    if 0 and 'Futter fuer den Generator':
        _('Invalid username %(username)r: character %(ch)r not allowed')

    def __init__(self, translate, username, ch):
        self.username = username
        self.ch = ch
        self.mkmsg(translate, username=username, ch=ch)


class InvalidStarter(InvalidChars):
    msgmask = ""'Invalid username %(username)r: ' \
                'must not start with %(ch)r'
    if 0 and 'Futter fuer den Generator':
        _('Invalid username %(username)r: must not start with %(ch)r')


class UsernameTooShort(InvalidUsername):
    msgmask = ""'Username %(username)r is too short; ' \
                'at least %(minlength)r characters required'
    if 0 and 'Futter fuer den Generator':
        _('Username %(username)r is too short; '
          'at least %(minlength)r characters required')

    def __init__(self, translate, username, minlength):
        self.username = username
        self.minlength = minlength
        self.mkmsg(translate, username=username, minlength=minlength)

class UsernameReserved(InvalidUsername):
    msgmask = (""'Username "%(username)s" is reserved.')

    def __init__(self, translate, username):
        self.username = username
        self.mkmsg(translate, username=username)
### ] ... Exception-Klassen für Benutzernamen-Überprüfung ]

class Browser(BrowserView):

    implements(IRegistrationBrowser)

    storageKey = 'registration'

    def setConfigure(self):
        """
        Speichere die Einstellungen der Registrierung
        """
        context = self.context
        checkperm = getToolByName(context, 'portal_membership').checkPermission
        if not checkperm('Manage portal', context):
            raise Unauthorized
        form = context.REQUEST.form

        portal = getToolByName(context, 'portal_url').getPortalObject()
        settings = portal.getBrowser('settings')

        settings._set(self.storageKey, form)

        message(context,
                'Changes saved.')
        return context.REQUEST.RESPONSE.redirect(context.REQUEST['HTTP_REFERER'])

    def getConfigure(self):
        """ """
        context = self.context

        portal = getToolByName(context, 'portal_url').getPortalObject()
        settings = portal.getBrowser('settings')

        return settings.get(self.storageKey, {})

    def set(self):
        """
        Fügt einen neuen Benutzer hinzu (anonyme Registrierung).
        Für administratives Hinzufügen siehe -> @@usermanagement.addUser
        """
        logger.info('----------- @@registration.set aufgerufen! -----------')
        return self.processNewUser(
                userid_field='username',
                afterwards='@@resolvei18n/cb3a946f352d552ac0e37b449af18d0c')

    # -------------------------- [ @@registration.processNewUser ... [
    def processNewUser(self, userid_field, afterwards=None,
                       silent=True):
        """
        Arbeitspferd für das Anlegen neuer Benutzer;
        verwendet sowohl von @@registration.set()
        als auch @@usermanagement.addUser()

        ACHTUNG, die neu angelegten Benutzer sind derzeit nicht einwandfrei!
        Siehe XXX-Kommentare
        """
        # TODO: kleinere Methoden extrahieren (zur Strukturierung, und für
        #       Wiederverwendbarkeit)
        context = self.context
        portal = getToolByName(context, 'portal_url').getPortalObject()

        # ggf. aktiven Admin ermitteln:
        pm = getToolByName(context, 'portal_membership')
        if pm.isAnonymousUser():
            creator = None
            cid = None
        else:
            auth_member = pm.getAuthenticatedMember()
            auth_id = str(auth_member)
            auth_fullname = auth_member.getProperty('fullname', auth_id) or auth_id or ''
            tup = (auth_id, auth_fullname)
            cid = tup[0]
            creator = '%s (%s)' % tup
        logger.info('creator is %s', creator)

        whitelist_fields = [
                userid_field,
                'firstname', 'lastname',
                'email',
                'locked', 'sendMail',
                ]
        sm = portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()

        transaction_active = False
        try:
            request = context.REQUEST
            form = request.form
            for key in whitelist_fields:
                try:
                    val = form[key]
                    if val and isinstance(val, six_string_types):
                        form[key] = val.strip()
                except KeyError:
                    pass

            userinfo = dict(form)
            if 'hostname' not in userinfo:
                userinfo['hostname'] = get_hostname(request)
            userinfo['ip'] = get_ip(request)
            # für Werte, die unter einem falschen Schlüssel aus dem Formular
            # kommen:
            for_author = {}

            translate = make_translator(context)  # ggf. auch den Import wieder löschen
            _ = translate

            try:
                username = form[userid_field]
                if username == cid:
                    logger.error('*** Etwas unerwartet: username %r'
                                 ' ist gleich dem des "creators" (%r)',
                                 username,
                                 cid)
                    creator = None
            except KeyError:
                # wenn das Registrierungsformular keinen separaten
                # Benutzernamen übergibt, ist das absichtlich so konfiguriert -
                # dann wird die E-Mail-Adresse verwendet
                if userid_field != 'email':
                    userid_field = 'email'
                    username = form[userid_field]
                else:
                    raise

            # wirft ggf. eine InvalidUsername(ValueError)-Exception:
            self.checkUserName(username, translate)

            form['fullname'] = form['firstname'] + ' ' + form['lastname']

            query = {}
            query['portal_type'] = 'UnitraccAuthor'
            # in @@registration.set wurde hier nach dem 'Creator' gesucht:
            query['getUserId'] = username

            # Look up user profile with specified username and create it
            # if it does not exist yet.
            puc = getToolByName(context, 'portal_user_catalog')
            if puc(query):
                raise ValueError(
                        _('User %(username)s already exists.'
                          ) % locals())

            ## [ Paßwort prüfen ... [
            try:
                if form['password'] != form['confirm_password']:
                    raise ValueError(
                            _('The password and the repetition '
                              'are not the same.'
                              ))
            except KeyError as e:
                logger.exception(e)
                raise ValueError(
                        _('error validating '
                          'the password and repetition'
                          ))

            password = context.getBrowser('password')
            password.validate(form['password'], translate=translate)
            ## ] ... Paßwort prüfen ]

            transaction.begin()
            transaction_active = True

            ## [ W3L ... [
            w3lok, w3lconfirm = None, None
            w3lmsg = None
            w3l = context.getBrowser('w3l')
            if w3l is not None:
                # present currently in zkb product only (wnzkb instance)
                logger.info('W3L-Anbindung vorhanden')
                skip_w3l = w3l.w3l_devmode() and form.get('suppress_w3l_user', False)
                if skip_w3l:
                    logger.info('Erzeugung des W3L-Benutzers %(username)r unterdrueckt',
                                locals())
                else:
                    w3lresult = w3l.processRegistration(
                                   creator=creator,
                                   pseudo=username,
                                   vorname=form['firstname'],
                                   nachname=form['lastname'],
                                   mail=form['email'])
                    w3lok = w3lresult['ok']
                    if not w3lok:
                        transaction.abort()
                        logger.info('Abbruch wg. W3L-Fehler')
                        return redirect(request['HTTP_REFERER'])
                    # Hier zwischendurch sichern!
                    # ansonsten bestünde die ID des Profils nur aus einem automatisch
                    # angehängten Suffix '-2' o.ä.
                    ## XXX vorstehende Symptomatik ist leider noch nicht behoben!
                    transaction.savepoint()
                    logger.info('commit (305)')
                    w3lconfirm = w3lresult['confirm']
                    w3lmsg = w3lresult['message']
            else:
                logger.info('Keine W3L-Anbindung')
            ## ] ... W3L ]

            PF_frueh = 1
            pm = getToolByName(context, 'portal_membership')
            try:
                # Create new portal member with the properties
                # given by the registration form
                logger.info('DEBUG Formulardaten fuer neuen User %r (addMember): %r',
                            username, subdict(form, keyfunc=no_password_fieldname))
                pm.addMember(id=username,
                             password=form['password'],
                             roles=('Member',),
                             domains='',
                             properties=form)
            except KeyError as e:
                # sollte eigentlich durch Profilsuche (s.o.) abgefangen
                # sein ...
                logger.error('error creating member: %s',
                             (str(e),
                              ))
                raise ValueError(
                        _('User %(username)s already exists.'
                          ) % locals())

            logger.info('added member %s', username)
            if creator is not None:
                message(context, _('added member %s'
                          ) % username)

            rc = getToolByName(context, 'reference_catalog')
            folder = rc.lookupObject(MEMBERSFOLDER_UID)  # -> '/management/autoren'
            userlog = context.getAdapter('userlog')

            if for_author:
                form.update(for_author)
            createObject = folder.getAdapter('createobject')
            try:
                object_ = createObject('UnitraccAuthor', form['fullname'].strip())
            except Unauthorized as e:
                logger.error('Konnte UnitraccAuthor %(username)r'
                             ' nicht anlegen (%(e)r)',
                             locals())
                logger.exception(e)
                raise
            else:
                object_.setUserId(username)
                logger.info('added profile %s', username)
                if PF_frueh:
                    object_.processForm(values=form)
                puc.catalog_object(object_)

            # [ Neuen Benutzer sperren? ... [
            LOCK_REASONS = []
            if form.get('locked'):  # Sperre durch Admin verlangt
                LOCK_REASONS.append('requested by admin')
            if creator is None:     # Selbst-Registrierung durch neuen Benutzer
                LOCK_REASONS.append('self-registration by anonymous')
            if w3lconfirm:
                # von W3L-Backend, um Kapern von Benutzern zu verhindern
                LOCK_REASONS.append('requested by w3l')

            if LOCK_REASONS:
                object_.setLocked(True)
                userinfo['locked'] = '; '.join(LOCK_REASONS)
                logger.info('lock for %s: %s', username, userinfo['locked'])
            else:
                logger.info('no lock for %s', username)
            # ] ... Neuen Benutzer sperren? ]

            # Hier zwischendurch sichern!
            # ansonsten bestünde die ID des Profils nur aus einem automatisch
            # angehängten Suffix '-2' o.ä.
            ## XXX vorstehende Symptomatik ist leider noch nicht behoben!
            ## Bei Verwendung von relationaler Datenbank sind
            ## Savepoints nicht verfügbar: Products.ZPsycopgDA.db.DB: Savepoints unsupported
            # transaction.savepoint()
            logger.info('savepoint (384)')

            logger.info('changeowner.set(%r) ...', username)
            changeowner = object_.getBrowser('changeowner')
            changeowner.set(username)
            logger.info('DEBUG Formulardaten (processForm): %r',
                        subdict(form, keyfunc=no_password_fieldname))
            if not PF_frueh:
                object_.processForm(values=form)
            object_.reindexObject()
            userinfo['uid (profile)'] = object_.UID()
            logger.info('processed profile %s', username)
            transaction.commit()
            transaction_active = False

            # Nachricht über W3L-User, für userlog:
            if w3lmsg is not None:
                userinfo['w3luser'] = w3lmsg
            if creator is None:
                logfunc = userlog.registered
            else:
                userinfo['by'] = creator
                logfunc = userlog.createdbyadmin
            logfunc(**userinfo)

            ## [ Mails senden ... [
            logger.info('Send mail? form.sendmail=%r, creator=%s', form.get('sendMail'), creator)
            if (form.get('sendMail')
                or creator is None
                or w3lconfirm
                ):
                try:
                    logger.info('calling sendBothRegistrationMails(%r, %r, ...',
                                object_, username)
                    self.sendBothRegistrationMails(object_, username, form)
                except MailHostError as e:
                    raise
                else:
                    if creator is None and not silent:
                        message(context, 'Thank you!'
                                ' Your user account was created.'
                                ' Please check your mail.'
                                )
            ## ] ... Mails senden ]
        except Unauthorized:
            if transaction_active:
                transaction.abort()
            raise
        except ReadOnlyError as e:
            message(context,
                    "Sorry; can't register while in read-only mode. "
                    'Please try again later. '
                    'Thank you!',
                    'error')
            raise
            return None
            return back_to_referer(request=request,
                                   items=[(key, form[key])
                                          for key in whitelist_fields
                                          if key in form
                                             and form[key] is not None
                                          ])
        except Exception as e:
            logger.error('%(e)s: aborting!', locals())
            logger.exception(e)
            done = False
            if isinstance(e, (InvalidUsername,
                              InvalidPassword,
                              ValueError,
                              )):
                try:
                    message(context, str(e),
                            'error')
                except Exception as e:
                    logger.error('%(e)s creating the message!', locals())
                    logger.exception(e)
                else:
                    done = True
            if not done:
                message(context,
                        'An unexpected error has occurred; '
                        'it has been logged, timestamp: "${timestamp}"',
                        'error',
                        mapping={'timestamp': strftime('%Y-%m-%d %H:%M:%S'),
                                 })
            if transaction_active:
                transaction.abort()
            return back_to_referer(request=request,
                                   items=[(key, form[key])
                                          for key in whitelist_fields
                                          if key in form
                                             and form[key] is not None
                                          ])
        else:
            if transaction_active:
                transaction.commit()

            if afterwards is None:
                return back_to_referer(request=request)
            else:
                return back_to_referer(request=request,
                                       url=afterwards)
        finally:
            sm.setOld()
        # ---------------------- ] ... @@registration.processNewUser ]

    @log_or_trace(debug_active, trace_key='sbrm', **lot_kwargs)
    def sendBothRegistrationMails(self, o, username, form=None):
        """
        Sende Registrierungs-Mails sowohl an den neuen Benutzer
        als auch an die konfigurierte administrative Adresse
        """
        context = self.context
        if form is None:    # ungetestet
            form = context.REQUEST.form
        if 'TAN' in form:
            if not 'tan' in form:
                form['tan'] = form.pop('TAN')
        tan = form.get('tan')

        # Create mail for user with activation link to unlock his account
        # Merge portal id into mail subject text
        portal_id = self.getPortalID()
        _ = make_translator(context)
        subject = _(""'mail_registration_user_subject') % locals()

        dict_ = {}
        dict_['fullname'] = o.getFirstname() + ' ' + o.getLastname()
        dict_['url'] = self.getActivationLink(o, tan=tan)

        mail = context.getBrowser('unitraccmail')
        mail.set('utf-8', 'mail_registration_user', subject, dict_)
        mail.renderAsPlainText(False)
        mail_from = self.getMailFrom()
        #             Absender   Empfänger
        mail.sendMail(mail_from, form['email'])
        logger.info('sent unlock link for %s from %s to %s',
                    username,
                    mail_from,
                    form['email'])

        # Create mail to notify site administration about user registration
        subject = 'Registrierungsbenachrichtigung für %(portal_id)s' \
                  % locals()

        dict_['email'] = form['email']
        dict_['username'] = username

        mail.set('utf-8', 'mail_registration_admin', subject, dict_)
        mail.renderAsPlainText()
        mail_bcc = self.getMailSiteAdmin()
        mail.sendMail(mail_from, mail_bcc)
        logger.info('sent info about registration of %s to %s',
                    username, mail_bcc)
        ### --------------------------- ...  sendBothRegistrationMails()

    def checkUserName(self,
                      username,
                      translate=None,
                      minlength=5,
                      propagate=True):
        """
        Überprüfe den übergebenen Namen auf Zulässigkeit und wirf ggf. eine
        Exception; für einen Wrapper incl. Auslesen des Formulars
        siehe -> @@registration.validateUserName()
        """
        if translate is None:
            translate = make_translator(self.context)
        try:
            if not username:
                raise EmptyUsername(translate, username)
            if ' ' in username:
                raise InvalidChars(translate, username, ' ')
            stripped = username.strip()
            if stripped != username:
                raise SurroundingBlanks(translate, username)
            if username.lower() in ('admin', 'administrator',
                                    'root', 'system',
                                    ):
                raise UsernameReserved(translate, username)
            if len(username) < minlength:
                raise UsernameTooShort(translate, username, minlength)
            return True
        except InvalidUsername:
            if propagate:
                raise
            return False

    def getActivationLink(self, profile, portal=None, tan=None):
        """
        Aktivierungslink für das übergebene Profilobjekt
        """
        if portal is None:
            portal = getToolByName(self.context, 'portal_url').getPortalObject()
        return makeActivationLink(profile, portal, tan)

    def validateUserName(self):
        """
        Prüfe den Benutzernamen auf Zulässig- und Verfügbarkeit

        Rückgabewert: ein Fehlertext oder, im Erfolgsfall: None
        """
        context = self.context
        form = context.REQUEST.form
        _ = make_translator(context)

        username = form.get('username', '')

        if not username:
            return _(""'Please enter a username.')

        try:
            w3l = context.getBrowser('w3l')
            if w3l is not None:
                w3l.checkPseudonym(username, True)
            self.checkUserName(username, _)
        except ValueError as e:
            ename = e.__class__.__name__
            logger.error('validateUserName(%(username)r): %(ename)s', locals())
            logger.exception(e)
            try:
                return str(e)
            except UnicodeEncodeError:
                return _('Invalid username')

        acl = getToolByName(context, 'acl_users')
        if acl.getUser(username):
            return _('Username "%s" already exists.'
                     ) % username
    # die Methode validateUserName wird im Rahmen der Registrierung verwendet
    # (fgvalidate_base); siehe auch --> checkUserName

    def validatePassword(self):
        """
        Formularfeld-Validierung, verwendet bei set-Methode
        (anonyme Selbstregistrierung)
        """
        context = self.context
        form = context.REQUEST.form
        acl = getToolByName(context, 'acl_users')
        _ = make_translator(context)

        password = form.get('password', '')
        confirm_password = form.get('confirm_password', '')

        if not password:
            return _(""'Please enter a password.')

        if password != confirm_password:
            return _(""'The new password and the repetition are not the same.')

        helper = context.getBrowser('password')
        try:
            helper.validate(password, _)
            return
        except ValueError as e:
            return str(e)
        except AttributeError as e:
            logger.error('!!! @@password nicht gefunden! !!!')
            logger.exception(e)
            raise

    def lock(self):
        context = self.context
        form = context.REQUEST.form
        rc = getToolByName(context, 'reference_catalog')

        uid = form.get('uid', '')

        object_ = rc.lookupObject(uid)
        object_.setLocked(True)
        object_.reindexObject()

    def _redirect(self, request, portal, path='/login_form'):
        """
        Leite zur Login- oder, wenn path angegeben, zu einer anderen Seite um
        """
        dest = portal.absolute_url() + path
        logger.info('redirecting to %(dest)r', locals())
        raise Redirect(dest)

    def unlock(self):
        """
        Die erstmalige Entsperrung (= der Benutzer war noch nie angemeldet)
        hat den Charakter einer Aktivierung.
        Sobald ein Benutzer einmal aktiviert **und angemeldet** war,
        funktioniert der unlock-Link nicht mehr; sonst könnte niemand
        wirksam gesperrt werden ...

        Problem:
        - wer sich noch nie angemeldet hat, kann nicht wirklich gesperrt werden
        - wer sich schon einmal angemeldet hat, muß "zurückgesetzt" werden
          (Anmeldedatum = Zeitpunkt Null), bevor der Unlock-Link wieder
          funktioniert.
        """
        context = self.context

        pm = getToolByName(context, 'portal_membership')
        if pm.isAnonymousUser():
            active_user = None
        else:
            auth_member = pm.getAuthenticatedMember()
            auth_id = str(auth_member)
            auth_fullname = auth_member.getProperty('fullname', auth_id) or auth_id or ''
            active_user = '%s (%s)' % (auth_id, auth_fullname)

        portal = getToolByName(context, 'portal_url').getPortalObject()

        request = context.REQUEST
        form = request.form

        sm = portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()

        transaction_active = False
        try:
            rc = getToolByName(context, 'reference_catalog')
            acl = getToolByName(context, 'acl_users')
            mail = context.getBrowser('unitraccmail')
            uid = form.get('uid', '')
            tan = form.get('tan', '')

            object_ = rc.lookupObject(uid)
            if object_ is None:
                logger.error('unlock: profile %r doesn\'t exist', uid)
                message(context,
                        'This account doesn\'t exist'
                        '; it may have been deleted'
                        '. Please contact the site administration.',
                        'error')
                if active_user is None:
                    return self._redirect(request, portal)

            userId = object_.getUserId()
            logger.info('unlock: profile %r --> user %r', uid, userId)
            user = acl.getUser(userId)
            if user is None:
                logger.error('unlock: user %r doesn\'t exist', userId)
                message(context,
                        'This account doesn\'t exist'
                        '; it may have been deleted'
                        '. Please contact the site administration.',
                        'error')
                if active_user is None:
                    return self._redirect(request, portal)

            login_time = user.getProperty('login_time')
            newUser = login_time == DateTime('2000/01/01')
            if not object_.getLocked():
                message(context, 'Your account has already been activated.')
            elif not newUser:
                # Ohne diese Prüfung könnte sich jeder stets mit seiner
                # ursprünglichen Aktivierungs-URL entsperren ...
                logger.info("Won't unlock non-new user %(user)r"
                            ' (login_time = %(login_time)r',
                            locals())
                message(context,
                        'Your account is locked'
                        '. Please contact the site administration.'
                        ,
                        'error')
                return self._redirect(request, portal, '')
            else:
                userlog = context.getAdapter('userlog')
                transaction.begin()
                transaction_active = True
                logger.info('unlock: transaction.begin')
                object_.setLocked(False)
                object_.reindexObject()
                message(context, 'Thank you! Your account has been activated.')

                dict_ = {}
                dict_['username'] = object_.getUserId()
                dict_['email'] = object_.getEmail()
                dict_['firstname'] = object_.getFirstname()
                dict_['lastname'] = object_.getLastname()
                dict_['forgot_password_link'] = portal.absolute_url() + '/mail_password_form'
                dict_['hostname'] = get_hostname(request)
                dict_['ip'] = get_ip(request)

                # Merge portal id into mail subject text
                _ = make_translator(context)
                subject = _('mail_confirmation_user_subject')
                subject = subject % {'portal_id': self.getPortalID()}

                # Create mail to notify user about account confirmation
                mail.set('utf-8', 'mail_confirmation_user', subject, dict_)
                mail.renderAsPlainText()
                mail_from = self.getMailFrom()
                mail.sendMail(mail_from, object_.getEmail())

                ## -------------- w3l-Registrierung jetzt komplett in
                ## -------------- Browser zkb@@w3l!

                # Create mail to notify site administration about user account confirmation
                subject = 'Registrierungsbestätigung für %(portal_id)s'
                subject = subject % {'portal_id': self.getPortalID()}

                dict_['username'] = object_.getUserId()
                dict_['email'] = object_.getEmail()
                dict_['fullname'] = object_.getFirstname() + ' ' + object_.getLastname()

                mail.set('utf-8', 'mail_confirmation_admin', subject, dict_)
                mail.renderAsPlainText()

                transaction.commit()
                logger.info('unlock: transaction.commit')
                transaction_active = False

                mail_bcc = self.getMailSiteAdmin()
                mail.sendMail(mail_from, mail_bcc)
                del dict_['fullname'], dict_['forgot_password_link']
                pm = getToolByName(context, 'portal_membership')
                if not pm.isAnonymousUser():
                    pm = getToolByName(context, 'portal_membership')
                    auth_member = pm.getAuthenticatedMember()
                    auth_id = str(auth_member)
                    auth_fullname = auth_member.getProperty('fullname', auth_id) or auth_id or ''
                    dict_['by'] = '%s (%s)' % (auth_id, auth_fullname)
                userlog.confirmed(**dict_)
            if tan:
                tail = '/mytan?tan=%(tan)s' % locals()
                return self._redirect(request, portal, tail)
            return self._redirect(request, portal)
        finally:
            if transaction_active:
                transaction.abort()
                logger.info('unlock: transaction.abort')
            sm.setOld()
        #if newUser:
        #    ppr = context.portal_password_reset
        #    dict_ = ppr.requestReset(object_.getUserId())
        #    return context.REQUEST.RESPONSE.redirect(portal.absolute_url()+'/pwreset_form?userid = '+object_.getUserId()+'&randomstring='+dict_['randomstring'])

    def getPortalID(self):
        """
        Get the "Portal ID" string parameter from UNITRACC registration configuration.

        Provides flexible rendering of portal id information within registration mails
        """
        portal_id = ""

        try:
            portal_id = self.getConfigure()['portal_id']
        except KeyError:
            portal_id = self.getPortalIDDefault()

        if not portal_id:
            portal_id = self.getPortalIDDefault()

        return portal_id

    def getMailFrom(self):
        """
        Ermittle die Absender-Adresse für Mails von der Benutzerregistrierung
        (Mailversand und -footer).
        Eine subportalspezifische Festlegung hat Vorrang;
        Beschriftung in configure_registration: "E-Mail From".
        """
        context = self.context
        subportal = context.getBrowser('subportal')
        if subportal is not None:
            mail_from = subportal.get_from_address('registration_from')
            if mail_from:
                return mail_from

        try:
            mail_from = self.getConfigure()['mailFrom']
        except KeyError:
            mail_from = self.getMailFromDefault()

        if not mail_from:
            mail_from = self.getMailFromDefault()

        return mail_from or ''

    def getMailSiteAdmin(self):
        """
        Ermittle die BCC-Adresse für Mails von der Benutzerregistrierung
        (Mailversand an neue Benutzer).
        Eine subportalspezifische Festlegung hat Vorrang;
        Beschriftung in configure_registration: "E-Mail Site Administration".
        """
        context = self.context
        subportal = context.getBrowser('subportal')
        mail_site_admin = subportal.get_from_address('registration_bcc')
        if mail_site_admin:
            return mail_site_admin

        try:
            mail_site_admin = self.getConfigure()['bcc']
        except KeyError:
            mail_site_admin = self.getMailSiteAdminDefault()

        if not mail_site_admin:
            mail_site_admin = self.getMailSiteAdminDefault()

        return mail_site_admin or ''

    def getPortalTitle(self):
        """
        Get the language specific "Portal Title" string parameter from UNITRACC registration configuration.

        Provides flexible rendering of registration emails
        """
        context = self.context

        langCode = getActiveLanguage(context)

        if langCode not in LANGUAGES:
            langCode = 'en'

        portal_title = ""

        try:
            portal_title = self.getConfigure()['portal_title_' + langCode]
        except KeyError:
            portal_title = self.getPortalTitleDefault()

        if not portal_title:
            portal_title = self.getPortalTitleDefault()

        return portal_title

    def getPortalDescription(self):
        """
        Get the language specific "Portal Description" string parameter from UNITRACC registration configuration.

        Provides flexible rendering of registration emails
        """
        context = self.context
        langCode = getActiveLanguage(context)

        if langCode not in LANGUAGES:
            langCode = 'en'

        portal_desc = ""

        try:
            portal_desc = self.getConfigure()['portal_description_' + langCode]
        except KeyError:
            portal_desc = self.getPortalDescriptionDefault()

        if not portal_desc:
            portal_desc = self.getPortalDescriptionDefault()

        return portal_desc

    def getPortalDomains(self):
        """
        Get the list "Portal Domains" from UNITRACC registration configuration.

        Provides flexible rendering of registration emails

        TODO: Subportale berücksichtigen!
        """
        portalDomains = []

        try:
            portalDomains = self.getConfigure()['portal_domains'].splitlines()
        except KeyError:
            logger.error('Kein @@setting %s[%r]',
                         self.storageKey, 'portal_domains')

        if not portalDomains:
            portalDomains = self.getPortalDomainsDefault()

        res = []
        for s in portalDomains:
            s = s.strip()
            if not s:
                continue
            res.append(make_url(s))
        return res

    def getPortalIDDefault(self):
        """
        Get default value for "Portal ID" for UNITRACC registration configuration.

        Provides default value if configuration value is not set
        """
        return "UNITRACC"

    def getMailFromDefault(self):
        """
        Get default value for "E-Mail From" parameter for UNITRACC registration configuration.

        Provides default value if configuration value is not set.
        """
        return "info@unitracc.de"

    def getMailSiteAdminDefault(self):
        """
        Get default value for "E-Mail Site Administration" parameter for UNITRACC registration configuration.

        Provides default value if configuration value is not set.
        """
        return "info@unitracc.de"

    def getPortalTitleDefault(self):
        """
        Get default value for "Portal Title" for UNITRACC registration configuration.

        Provides default value if configuration value ist not set.
        """
        context = self.context
        langCode = getActiveLanguage(context)

        defaults = {'de': 'UNITRACC - Underground Infrastructure Training and Competence Center',
                    'en': 'UNITRACC - Underground Infrastructure Training and Competence Center',
                    'es': 'UNITRACC - Underground Infrastructure Training and Competence Center',
                   }

        return defaults.get(langCode, 'UNITRACC - Underground Infrastructure Training and Competence Center')

    def getPortalDescriptionDefault(self):
        """
        Get default value for "Portal Description" for UNITRACC registration configuration.

        Provides default value if configuration value ist not set.
        """
        context = self.context
        langCode = getActiveLanguage(context)

        defaults = {'de': 'Webbasierte Informations-, Lehr-, Lern- und Arbeitsplattform für den Kanal- und Rohrleitungsbau',
                    'en': 'Web-based information, teaching and working platform for sewer and pipeline construction',
                    'es': 'Plataforma de aprendizaje, de información y de trabajo en línea para la construcción de alcantarillados y tuberías',
                   }

        return defaults.get(langCode, 'Webbasierte Informations,- Lehr-, Lern- und Arbeitsplattform für den Kanal- und Rohrleitungsbau')

    def getPortalDomainsDefault(self):
        """
        Get default list "Portal Domains" for UNITRACC registration configuration.

        Provides default list if configuration list is not set.
        """
        return ["www.unitracc.de",
                "www.unitracc.com",
                "www.unitracc.es",
                ]
