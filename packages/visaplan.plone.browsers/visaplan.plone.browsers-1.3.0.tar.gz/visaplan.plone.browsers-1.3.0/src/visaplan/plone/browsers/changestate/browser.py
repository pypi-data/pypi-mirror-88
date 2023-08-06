# -*- coding: utf-8 -*- äöü
# Python compatibility:
from __future__ import absolute_import

# Zope:
import transaction
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

# 3rd party:
from bs4 import BeautifulSoup

# visaplan:
from visaplan.kitchen.spoons import extract_uids
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.context import make_translator, message
from visaplan.tools.coding import safe_decode

# Local imports:
from .data import initial_publication_transition
from .utils import (
    make_reference_errors_msg,
    make_reference_errors_msg_html,
    make_reference_success_msg,
    make_reference_success_msg_html,
    )

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import log_or_trace, pp

logger, debug_active, DEBUG = getLogSupport(fn=__file__)
TRACE = None

# -------------------------------------------- [ Daten ... [
lot_kwargs = {'debug_level': debug_active,
              'logger': logger,
              'trace': 0,
              }
PUBLISHING_TRANSITIONS = frozenset([
    'make_public',
    'make_visible',
    'make_restricted',
    # auch die reduzierenden:
    'make_visible_again',
    'make_restricted_again',
    # historisch / Dayta-Workflow:
    'make_approved',
    ])
REDUCING_TRANSITIONS = frozenset([
    'make_retract',
    'make_rejected',
    # Transitionen des Unitracc-Workflows:
    'make_private_again',
    'make_visible_again',
    'make_restricted_again',
    ])
SOUP = 1
HTML_MSGs = True
# -------------------------------------------- ] ... Daten ]


class IChangeState(Interface):

    def set():
        """
        Setzt den neuen Workflow-Status für das aufrufende Objekt - und ggf. die
        von ihm textuell eingebundenen - durch Aufruf von Übergängen
        (Transitionen).
        """


class Browser(BrowserView):

    implements(IChangeState)

    @log_or_trace(**lot_kwargs)
    def set(self):
        """
        Setzt den neuen Workflow-Status für das aufrufende Objekt - und ggf. die
        von ihm textuell eingebundenen - durch Aufruf von Übergängen
        (Transitionen).

        Eine Sonderrolle spielte im *alten* <dayta_workflow> der Zustand (Status)
        "approved": wird er gesetzt, so wird für das aufrufende Objekt der je
        nach Typ festgelegte Standard-Veröffentlichungszustand gewählt (siehe
        .data.initial_publication_transition; gf: ./data.py).

        Siehe auch den Browser dayta@@workflow, gf:
        ../../../../lib/python2.7/site-packages/dayta/browser/workflow/browser.py
        """
        context = self.getContext()
        form = context.REQUEST.form
        portal = getToolByName(context, 'portal_url').getPortalObject()

        contextUid = context.UID()

        # -------------------- [ UIDs weiterer Objekte ermitteln ... [
        # TODO: Referenzen aus reference_catalog verwenden
        strings = []
        for field in context.schema.fields():
            if getattr(field, 'default_output_type', '') == 'text/html':
                more = field.get(context)
                if more:
                    strings.append(safe_decode(more))
        string_ = u' '.join(strings)

        transform = context.getBrowser('transform')

        string_ += u' ' + transform.get(string_)
        if SOUP:
            soup = BeautifulSoup(string_)
            list_ = list(extract_uids(soup))
            logger.info('set: Found %d UIDs using BeautifulSoup', len(list_))
        else:
            list_ = []
            for imgTag in set(transform._getImages(string_)):
                list_.append(transform._getImgUid(imgTag))

            for aTag in set(transform._getLinks(string_)):
                uid, targetUid = transform._getUid(aTag)
                if uid:
                    list_.append(uid)
            logger.info('set: Found %d UIDs by regular expressions', len(list_))
        if list_:
            list_ = sorted(set(list_))
            logger.info('set: %d *different* UIDs', len(list_))
        # -------------------- ] ... UIDs weiterer Objekte ermitteln ]

        wa = workflow_action = form.get('workflow_action')
        changes = 0
        maintaskdone = False
        logger.info('%(context)r.set(%(workflow_action)r) ...', locals())
        rc = getToolByName(context, 'reference_catalog')
        if workflow_action in PUBLISHING_TRANSITIONS:
            mediathek = portal.getBrowser('mediathek')
        move_kwargs = {'rc': rc,
                       # 'use_transaction': USE_TRANSACTION,
                       }
        success_list = []
        errors_list = []
        notfound_list = []
        for uid in list_:
            formsg = {'uid': uid,
                      }
            object_ = rc.lookupObject(uid)
            if object_:
                formsg['o'] = object_
                workflow = object_.getBrowser('workflow')
                # Rückgabewert erfordert evtl. dayta-Zweig therp:
                if workflow.change(workflow_action):
                    changes += 1
                    logger.info('set(%(wa)r): object %(uid)r (%(object_)r) changed', locals())
                    success_list.append(formsg)
                else:
                    logger.error('set(%(wa)r): object %(uid)r (%(object_)r) not proceeded', locals())
                    errors_list.append(formsg)

                if workflow_action in PUBLISHING_TRANSITIONS:
                    if mediathek._move(o=object_, **move_kwargs):
                        changes += 1
                    # kommt nur vor im Dayta-Workflow:
                    if workflow_action == 'make_approved':
                        self._setInitialPublishedState(object_)
                transaction.savepoint()
            else:
                logger.error('set: object %(uid)r not found', locals())
                notfound_list.append(formsg)

        # return context.restrictedTraverse('msgbox')(**kw)
        # message (HTML), messageType, errText

        workflow = context.getBrowser('workflow')
        if workflow.change(workflow_action):
            changes += 1
            maintaskdone = True
        if workflow_action in PUBLISHING_TRANSITIONS:
            if mediathek._move(o=context, **move_kwargs):
                changes += 1
            # kommt nur vor im Dayta-Workflow:
            if workflow_action == 'make_approved':
                self._setInitialPublishedState(context)
        transaction.commit()

        if maintaskdone or success_list:
          _ = translate = make_translator(context)
          try:
            if maintaskdone:
                # Wg. Extraktion durch pot-create (lingua):
                mwa = u'mwa_' + workflow_action
                msg = _(mwa,
                        mapping={u'title': safe_decode(context.Title()),
                                 })
                message(context, msg)
          except UnicodeError as e:
                logger.error('Error creating success message %(workflow_action)r for %(context)r', locals())
                logger.exception()
          finally:
            msgbox = context.restrictedTraverse('msgbox')
            pu = getToolByName(context, 'plone_utils')
            pu_aPM = pu.addPortalMessage
            if HTML_MSGs:  # ---------- [ HTML-Meldungen erzeugen ... [
                txt = make_reference_success_msg_html(success_list, translate)
                if txt:
                    pu_aPM(txt, 'structure')

                txt = make_reference_errors_msg_html(notfound_list, errors_list, translate)
                if txt:
                    pu_aPM(txt, 'structure')
            else:  # ------- ] ... HTML-, Text-Meldungen erzeugen ... [
                txt = make_reference_success_msg(success_list, translate)
                if txt:
                    pu_aPM(txt, 'info')

                txt = make_reference_errors_msg(notfound_list, errors_list, translate)
                if txt:
                    pu_aPM(txt, 'error')
            # ------------------------- ] ... Text-Meldungen erzeugen ]
        else:
            try:
                message(context, u'Error executing "${workflow_action}"!',
                    'error',
                    mapping=locals())
            except UnicodeError as e:
                logger.error('Error creating error message %(workflow_action)r for %(context)r', locals())
                logger.exception()

        return context.REQUEST.RESPONSE.redirect(portal.absolute_url() + '/@@resolveuid/' + contextUid + '/view?time=' + str(DateTime().millis()))

    def _setInitialPublishedState(self, object):
        """
        Achtung:
            Seit der Überarbeitung des Dayta-Workflows (zwischenzeitlich
            <unitracc_workflow>) gibt es keinen Übergang <make_approved> mehr -
            daher ist das nun "toter Code!"

        Bei Aktivierung des Freigabestatus "approved" (freigegeben) (stets
        durch den Übergang "make_approved") wird die Veröffentlichungsstufe des
        übergebenen Objekts
        - mit steigender Öffentlichkeit: für Teilnehmer, für Angemeldete, für alle -
        in Abhängigkeit vom Objekttyp festgelegt.
        """
        if not object:
            logger.info('_sIPS: object is %(object)r; terminating', locals())
            return
        pt = object.portal_type
        # ID des auszuführenden Übergangs:
        transition = initial_publication_transition[pt]
        if transition is None:
            logger.warning('_sIPS(%(object)r): portal_type=%(pt)r; NO KNOWN TRANSITION!', locals())
            return

        rc = getToolByName(object, 'reference_catalog')
        uid = object.UID()
        logger.info('_sIPS(): %r --> transition %r', object, transition)
        object.getBrowser('workflow').change(transition)
        object = rc.lookupObject(uid)
        logger.info('_sIPS(...): object=%(object)r', locals())
        object.reindexObject()


# zum suchen:
## mwa_make_public
## mwa_make_approved
## mwa_make_visible
## mwa_make_restricted
