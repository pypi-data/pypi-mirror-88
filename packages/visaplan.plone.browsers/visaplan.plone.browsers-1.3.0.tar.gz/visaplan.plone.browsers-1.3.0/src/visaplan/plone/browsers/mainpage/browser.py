# -*- coding: utf-8 -*- äöü  vim: tw=79
# Python compatibility:
from __future__ import absolute_import, print_function

# Zope:
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.context import (
    get_published_templateid,
    make_pathByUIDGetter,
    )

# Vorgabewert fuer Startseite (als UID)
DEFAULT_PAGE_UID = 'f1bce398a8269e3b5f468373596e9a0c'

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import log_or_trace, pp

logger, debug_active, DEBUG = getLogSupport()

lot_kwargs = {'logger': logger,
              'debug_level': debug_active,
              }

# Local imports:
from .data import NOSEARCH_IDS, NOSEARCH_PREFIXES


class IMainpage(Interface):

    def get_mainpage():
        """Liefert Sprach und Subportal abhaengig die korrekte Seite zurueck"""

    def get_banner_context():
        """ """

    def configured_page_uid(dic=None):
        """
        Gib die konfigurierte Startseiten-UID oder den Vorgabewert zurück
        """

    def show_search_login():
        """
        Soll das Suchformular ausgegeben werden?

        Historisch:
        "Soll die Suche und das Login gezeigt werden?"
        Das war aber Unsinn - beide haben nichts miteinander zu tun.
        Das Login-Formular wird ausgegeben, wenn der aktuelle Benutzer nicht
        angemeldet ist.
        """


class Browser(BrowserView):

    implements(IMainpage)

    config_storage_key = 'config_mainpage'

    def get_banner_context(self):

        context = self.context
        request = context.REQUEST

        if 'VIRTUAL_URL_PARTS' in request and request['VIRTUAL_URL_PARTS'][1]:
            """
            Virtual_URL_PARTS = (server-url, parameter OR '')
            nicht auf der Startseite; keinen Context zurueckgeben
            """
            return None

        if context.portal_type == 'Plone Site':
            return self.get_mainpage()
        return context

    @log_or_trace(**lot_kwargs)
    def get_mainpage(self):
        """
        Wenn eine folder_uid konfiguriert ist ("Main page folder uid"), gib das
        erste Dokument zurück, das unter diesem Ordner gefunden wird.

        Andernfalls gib die Seite mit der UID <page_uid> zurück ("Fallback
        default page uid", Standardwert: 'f1bce398a8269e3b5f468373596e9a0c').
        """

        context = self.context

        rc = getToolByName(context, 'reference_catalog')
        pc = getToolByName(context, 'portal_catalog')
        dict_ = self._get_config()

        folder_uid = dict_.get('folder_uid')
        if folder_uid:
            uid2path = make_pathByUIDGetter(context)
            query = {}
            query['portal_type'] = 'Document'
            query['sort_on'] = 'getObjPositionInParent'
            query['path'] = {'query': uid2path(folder_uid),
                             'depth': 1}
            if 0:
                pp(query=query)

            # Nur Suchen, wenn folder_uid konfiguriert:
            brains = pc(query)

            #Es darf hier zwingend nur ein Element zurueckkommen. Es gibt nur eine Startseite.
            #Wird gar nix gefunden. Deutsche Startseite als fallback.
            if brains:
                o = brains[0].getObject()
                try:
                    o_uid = o.UID()
                    return o
                except Exception as e:
                    print('!!!', e)

        page_uid = self.configured_page_uid(dict_)
        return rc.lookupObject(page_uid)

    def configured_page_uid(self, dic=None):
        """
        Gib die konfigurierte Startseiten-UID oder den Vorgabewert zurück
        """
        if dic is None:
            dic = self._get_config()
        return dic.get('page_uid', DEFAULT_PAGE_UID) or DEFAULT_PAGE_UID

    @log_or_trace(**lot_kwargs)
    def _get_config(self):

        context = self.context
        settings = context.getBrowser('settings')
        return settings.get(self.config_storage_key, {})

    @log_or_trace(**lot_kwargs)
    def show_search_login(self):
        """
        Soll das Suchformular ausgegeben werden?

        Historisch:
        "Soll die Suche und das Login gezeigt werden?"
        Das war aber Unsinn - beide haben nichts miteinander zu tun.
        Das Login-Formular wird ausgegeben, wenn der aktuelle Benutzer nicht
        angemeldet ist.
        """
        context = self.context
        template = get_published_templateid(context)
        logger.debug('show_search_login: template=%(template)r', locals())

        if template is None:
            return True

        if template in NOSEARCH_IDS:
            logger.debug('show_search_login: NOSEARCH id match %(template)r',
                         locals())
            return False

        match = template.startswith
        for prefix in NOSEARCH_PREFIXES:
            if match(prefix):
                logger.debug('show_search_login: NOSEARCH prefix match'
                             ' (%(template)r.startswith %(prefix)r)',
                            locals())
                return False

        return True
