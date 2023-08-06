# -*- coding: utf-8 -*- äöü
# Python compatibility:
from __future__ import absolute_import, print_function

from six import text_type as six_text_type

# Standard library:
import email
from copy import deepcopy
from email.utils import formataddr, getaddresses

# Zope:
from App.config import getConfiguration
from Products.CMFCore.utils import getToolByName
from Products.MailHost.MailHost import MailHostError

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.tools.html import _unicode_without_bom

# Local imports:
from .kitchen import html2plain
## Mail-Modul von Christian Heimes (Abhängigkeit eliminieren?):
from .mail import Mail
from .utils import (
    emailListToString,
    encodeHeaderAddress,
    harden_linebreaks,
    setHeaderOf,
    validateSingleEmailAddress,
    )

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import log_or_trace, pp

LOGGER, debug_active, DEBUG = getLogSupport()
# TODO: Separate Konfiguration für Logging
log_active = debug_active

lot_kwargs = {'logger': LOGGER,
              'trace': debug_active > 1,
              'verbose': True,
              }


class IUnitraccMail(Interface):
    """
    Neuer Mailer für Unitracc
    """

    def sendMail(mailFrom, mailTo, inReplyTo='', mbcc=None):
        """ """


class Browser(BrowserView):

    implements(IUnitraccMail)

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)

    def set(self, charset, template_id, subject, kwargs={}):
        self.charset = charset
        self.template_id = template_id
        self.subject = subject
        self.kwargs = kwargs

    def renderAsPlainText(self, convert=True):
        """
        Verwende das konfigurierte Template (.set) zur Generierung des
        Textkörpers, konvertiere das Ergebnis ggf. zu einfachem Text
        und setze den MIME-Typ auf text/plain.

        Achtung:
        - Es wird bislang nur eine HTML-Untermenge unterstützt
          (siehe Modul .kitchen bzw. die Funktion html2plain);
          bei noch nicht implementierten HTML-Elementen tritt ein Fehler auf!
        - Wenn das Template schon text/plain erzeugt, muß die Konversion
          unterdrückt werden! (convert=False übergeben)
        """
        template = self._getTemplate()
        text = template(**self.kwargs)
        if debug_active:
            print('--- renderAsPlainText(%r), head: %r' % (template, text[:10]))
        if convert:
            text = html2plain(text)
            if debug_active:
                print(('--- renderAsPlainText(%r), head: %r'
                       ) % (template, text[:10]))
        else:
            # sonst von html2plain --> collapse_whitespace erledigt:
            text = _unicode_without_bom(text)
            # Vor "Optimierung" durch Outlook schützen:
            text = harden_linebreaks(text)
        self.email = text.encode(self.charset)
        self.subtype = 'plain'
        if debug_active:
            print('------------- renderAsPlainText ... ------------')
            print(self.email)
            print('------------- ... renderAsPlainText ------------')

    def _getTemplate(self):
        """return template as object"""
        return self.context.unrestrictedTraverse(self.template_id)

    def renderAsHTML(self):
        """
        Verwende das übergebenen Template zur Generierung des Textkörpers
        und setze den MIME-Typ auf text/html

        Achtung:
        - Mails, die *nur* einen HTML-Teil enthalten, findet SpamAssassin unfein!
          Der Browser unterstützt leider derzeit noch keine mehrteiligen Mails.

        TODO:
        - bei HTML-Mails aus dem Template generell auch einen text/plain-Teil
          erzeugen
        """
        # return self.renderAsPlainText()

        template = self._getTemplate()
        self.email = str(template(**self.kwargs))
        if debug_active:
            print('------------- renderAsHTML ... ------------')
            print(self.email)
            print('------------- ... renderAsHTML ------------')
        self.subtype = 'html'

    @log_or_trace(debug_active, trace_key='sendMail', **lot_kwargs)
    def sendMail(self, mailFrom, mailTo, inReplyTo='', mbcc=None):

        context = self.context

        logging = context.getBrowser('logging')

        try:
            self._send_mail(self.email, mailTo, mailFrom, self.subject,
                            None, mbcc, self.subtype, self.charset, False,
                            **{'Reply-To': inReplyTo})
        except Exception as e:
            logging.log(mail_browser_error=str(e))
            LOGGER.exception(e)
            return

        if log_active:
            logging.log(dummy='_' * 80)
            logging.log(subject=self.subject)
            logging.log(mail_from=mailFrom)
            logging.log(mail_to=mailTo)
            logging.log(subtype=self.subtype)

            if mbcc:
                logging.log(mbcc=mbcc)
            if inReplyTo:
                logging.log(in_reply_to=inReplyTo)

            logging.log(email=self.email)

    @log_or_trace(debug_active, **lot_kwargs)
    def _send_mail(self, message, mto, mfrom, subject='[No Subject]',
                   mcc=None, mbcc=None, subtype='plain', charset='us-ascii',
                   debug=False, inReplyTo='', **kwargs):
        """A more secure way to send a message

        message:
            The plain message text without any headers or an
            email.Message.Message based instance
        mto:
            To: field (string or list)
        mfrom:
            From: field
        subject:
            Message subject (default: [No Subject])
        mcc:
            Cc: (carbon copy) field (string or list)
        mbcc:
            Bcc: (blind carbon copy) field (string or list)
        subtype:
            Content subtype of the email e.g. 'plain' for text/plain (ignored
            if message is a email.Message.Message instance)
        charset:
            Charset used for the email, subject and email addresses
        kwargs:
            Additional headers
        """
        mto = emailListToString(mto)
        mcc = emailListToString(mcc)
        mbcc = emailListToString(mbcc)
        # validate email addresses
        # XXX check Return-Path
        for addr in mto, mcc, mbcc:
            if addr:
                result = validateSingleEmailAddress(addr)
                if not result:
                    raise MailHostError('Invalid email address: %s' % addr)
        result = validateSingleEmailAddress(mfrom)
        if not result:
            raise MailHostError('Invalid email address: %s' % mfrom)

        # create message
        if isinstance(message, email.Message.Message):
            # got an email message. Make a deepcopy because we don't want to
            # change the message
            msg = deepcopy(message)
        else:
            if isinstance(message, six_text_type):
                message = message.encode(charset)
            msg = email.MIMEText.MIMEText(message, subtype, charset)

        mfrom = encodeHeaderAddress(mfrom, charset)
        mto = encodeHeaderAddress(mto, charset)
        mcc = encodeHeaderAddress(mcc, charset)
        mbcc = encodeHeaderAddress(mbcc, charset)

        # set important headers
        setHeaderOf(msg, skipEmpty=True, From=mfrom, To=mto,
                 Subject=str(email.Header.Header(subject, charset)),
                 Cc=mcc, Bcc=mbcc)

        setHeaderOf(msg, **kwargs)

        if inReplyTo:
            msg['Reply-To'] = encodeHeaderAddress(inReplyTo, charset)

        # we have to pass *all* recipient email addresses to the
        # send method because the smtp server doesn't add CC and BCC to
        # the list of recipients
        to = msg.get_all('to', [])
        cc = msg.get_all('cc', [])
        bcc = msg.get_all('bcc', [])
        #resent_tos = msg.get_all('resent-to', [])
        #resent_ccs = msg.get_all('resent-cc', [])
        recipient_list = getaddresses(to + cc + bcc)
        all_recipients = [formataddr(pair) for pair in recipient_list]

        # finally send email
        return self._send(mfrom, all_recipients, msg, debug)

    @log_or_trace(debug_active, **lot_kwargs)
    def _send(self, mfrom, mto, messageText, debug=False):
        """Send the message
        """
        context = self.context
        portal = getToolByName(context, 'portal_url').getPortalObject()
        mailhost = portal.MailHost

        if not isinstance(messageText, email.Message.Message):
            message = email.message_from_string(messageText)
        else:
            message = messageText
        smtp_notls = getattr(mailhost, 'smtp_notls', False)

        mail = Mail(mfrom, mto, message,
                    smtp_host=mailhost.smtp_host,
                    smtp_port=mailhost.smtp_port,
                    userid=mailhost.smtp_uid,
                    password=mailhost.smtp_pwd,
                    notls=smtp_notls
                    )
        if debug:
            print('------------- _send(debug) ... ------------')
            print(mail)
            print('------------- ... _send(debug) ------------')
            return mail
        else:
            DEBUG('Sending mail to %(mto)s ...', locals())
            res = mail.send()
            DEBUG('... mail to %(mto)s sent --> %(res)r', locals())
