# -*- coding: utf-8 -*- äöü
# Python compatibility:
from __future__ import absolute_import

# Zope:
from AccessControl import Unauthorized
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.base.permissions import (  # v.p.base v1.1.3.dev1+:
    ADD_STRUCTURE_TYPES,
    COPY_STRUCTURE_TYPES,
    DELETE_STRUCTURE_TYPES,
    MANAGE_EXPORT_PROFILES,
    MANAGE_KEYWORDS,
    MANAGE_ORDERS,
    MANAGE_STRUCTURE_TYPES,
    MANAGE_SUBMITTED_AND_ACCEPTED_CONTENT,
    MANAGE_TANS,
    PUBLISH_STRUCTURE_TYPES,
    ManageCourses,
    ManageGroups,
    ManageUsers,
    View_Development_Information,
    )
from visaplan.plone.tools.context import make_permissionChecker
from visaplan.plone.tools.decorators import returns_json
from visaplan.tools.dicts import getOption
from visaplan.tools.minifuncs import check_kwargs

# Local imports:
from .utils import jsonify

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport

LOGGER, debug_active, DEBUG = getLogSupport(defaultFromDevMode=False)
sw_kwargs = {'enable': bool(debug_active),
             'logger': LOGGER,
             }


class IManagementBrowser(Interface):

    def getStructureElementFolders():
        """ """

    def getSubmittedContent():
        """
        Gib alle Objekte im Bearbeitungsstatus "eingereicht" zurück
        """

    def getAcceptedContent():
        """
        Gib alle Objekte im Bearbeitungsstatus "akzeptiert" zurück
        """

    def getManagedContent():
        """
        Gib die Objekte der Bearbeitungsliste zurück;
        entnimm den Bearbeitungsstatus den Formulardaten
        """

    def getManagedContent_ajax():
        """
        Gib die Objekte der Bearbeitungsliste im JSON-Format zurück
        """

    def canAccessSiteManagement():
        """
        Zugriff auf die Unitracc-Verwaltungsseiten (wenn auch nicht
        notwendigerweise alle) erlaubt?
        """

    def canAccessStage():
        """
        Zugriff auf die Buehne erlaubt?
        """

    def get_management_actions():
        """ """

    def getJavascriptDatatables(state):
        """
        Return the Javascript code to create the DataTables
        """

    def review_data_json():
        """
        Daten für dataTable({ajax: {url, dataSrc: ''}});
        @returns_json
        """

    def isDeveloper():
        """
        Darf der angemeldete Benutzer Entwicklerinformationen sehen?

        Es wird eine Berechtigung geprüft, keine Rolle; der Name wurde im Sinne
        der Handlichkeit gewählt.
        """


class Browser(BrowserView):

    implements(IManagementBrowser)

    def getStructureElementFolders(self):
        """ """
        context = self.context
        storagefolder = context.getBrowser('storagefolder')

        list_ = []

        for aname in (
            'getVirtualConstructionFolder',
            'getTechnicalInformationFolder',
            'getInstructionsFolder',
            'getDocumentationFolder',
            'getPaperFolder',
            'getPresentationFolder',
            ):
            a = getattr(storagefolder, aname)
            try:
                list_.append(a())
            except Exception as e:
                LOGGER.exception(e)

        return list_

    def getSubmittedContent(self):
        """
        Gib alle Objekte im Bearbeitungsstatus "eingereicht" zurück
        """
        return self._getManagedContent('submitted')

    def _getManagedContent(self, review_state, **kwargs):

        context = self.context
        checkperm = getToolByName(context, 'portal_membership').checkPermission
        if not checkperm('unitracc: Manage submitted and accepted content', context):
            raise Unauthorized

        query = {
            'Language': 'all',
            'sort_on': 'modified',
            'sort_order': 'descending',
            'NO_SUBPORTAL': 1,
            }
        if review_state:
            query['review_state'] = review_state

        modified_after = kwargs.pop('modified_after', None)
        max_age = kwargs.pop('max_age', None)
        all = kwargs.pop('all', None)
        limit = kwargs.pop('limit', not all and 100 or None)
        if limit:
            query['sort_limit'] = limit
        if all is None:
            all = modified_after is None and max_age is None
        if not all:
            if modified_after is None:
                if max_age is None:
                    max_age = 365
                else:
                    max_age = int(max_age)
                if max_age > 0:
                    modified_after = DateTime() - max_age
            if modified_after is not None:
                query['modified'] = {
                    'query': modified_after,
                    'range': 'min',
                    }
        check_kwargs(kwargs)  # raises TypeError if necessary

        pc = getToolByName(context, 'portal_catalog')
        res = pc(**query)
        return res

    def getAcceptedContent(self):
        """
        Gib alle Objekte im Bearbeitungsstatus "akzeptiert" zurück
        """
        return self._getManagedContent('accepted')

    def getManagedContent(self):
        """
        Gib die Objekte der Bearbeitungsliste zurück;
        entnimm den Bearbeitungsstatus den Formulardaten
        """
        context = self.context
        form = context.REQUEST.form
        review_state = getOption(form, 'review_state')
        return self._getManagedContent(review_state)

    def getManagedContent_ajax(self):
        """
        Gib die Objekte der Bearbeitungsliste im JSON-Format zurück
        """
        return jsonify(context, self.getManagedContent())

    def _getManagedContent_json(self, review_state, varname=None, **kwargs):
        """
        Gib die Objekte der Bearbeitungsliste im JSON-Format zurück

        (Das separate script-Element, in dem die Variable <varname> zugewiesen
        wurde, wurde aus templates/review_submitted_content.pt entfernt)
        """
        return jsonify(self.context,
                self._getManagedContent(review_state,
                                        **kwargs),
                varname)

    def canAccessSiteManagement(self, raiseUnauthorized=False):
        """
        Checks if current user can access site administration.
        @param raiseUnauthorized Raises Unauthorized if parameter value is True user can not access site management
        """
        cp = make_permissionChecker(self.context, verbose=debug_active)
        canAccess = (cp('Manage portal') or
                     cp(ManageUsers) or
                     cp(ManageGroups) or
                     cp(ManageCourses) or
                     cp(MANAGE_KEYWORDS) or
                     cp(MANAGE_SUBMITTED_AND_ACCEPTED_CONTENT) or
                     cp(MANAGE_STRUCTURE_TYPES) or
                     cp(ADD_STRUCTURE_TYPES) or
                     cp(COPY_STRUCTURE_TYPES) or
                     cp(DELETE_STRUCTURE_TYPES) or
                     cp(PUBLISH_STRUCTURE_TYPES) or
                     cp(MANAGE_ORDERS) or
                     cp(MANAGE_EXPORT_PROFILES) or
                     cp(MANAGE_TANS))

        if not canAccess and raiseUnauthorized:
            raise Unauthorized

        return canAccess

    def canAccessStage(self, raiseUnauthorized=False):
        """
        Zugriff auf die Buehne erlaubt?
        @param raiseUnauthorized Wenn True, wird ggf. eine
                                 Unauthorized-Exception geworfen
        """
        cp = make_permissionChecker(self.context, verbose=debug_active)
        if (cp('stage: Manage stage') or
            cp('unitracc: Manage Ads')):
            return True
        elif raiseUnauthorized:
            raise Unauthorized
        else:
            return False

    def _zopesrv_url(self):
        """
        Gib die mitmaßliche URL des Zope-Servers zurück;
        die Kombination 'http://%(SERVER_NAME)s:%(SERVER_PORT)s/'
        hat sich (aufgrund suboptimaler DNS-Konfiguration?)
        als unzuverlässig erwiesen
        """
        context = self.context
        request = context.REQUEST
        get = request.get
        port = get('SERVER_PORT')
        name = get('SERVER_NAME')
        if name in ('local',  # z. B. visaplan-Netz
                    'test',   # Test-Instanzen
                    ):
            xhost = get('HTTP_X_FORWARDED_HOST')
            if xhost:
                hostl = xhost.split('.', 1)
                if hostl[1:]:
                    host = hostl[1]
                    return 'http://%(host)s:%(port)s' % locals()
        # Zope selbst verwendet stets http, nicht https:
        return 'http://%(name)s:%(port)s' % locals()

    def get_management_actions(self):

        context = self.context

        if not getToolByName(context, 'portal_membership').checkPermission('Manage portal', context):
            raise Unauthorized

        pa = getToolByName(context, 'portal_actions')

        navigation = context.getBrowser('navigation')

        list_ = []

        for id in pa.objectIds():
            if id.startswith('management_'):
                list_.extend(navigation.get_actions([id]))
        return list_

    def getJavascriptDatatables(self, state):
        """
        Return the Javascript code to create the DataTables
        """
        request = self.context.REQUEST
        kwargs = {}
        all = request.get('all', False)
        if all:
            kwargs['all'] = all
        data = self._getManagedContent_json(state, **kwargs)
        return ("""\
$(document).ready(function () {
    $('table.objects').dataTable({
            sDom: Unitracc.sDom_12,
            data: %(data)s,
            columns: [
                    {render:
                        function (data, type, row, meta) {
                            return '<a href="'+row.view_url+'">'+row.title+'</a>'
                        }
                     },
                    {data: 'creator_name'},
                    {data: 'portal_type'},
                    {data: 'modification_time'},
                    {data: 'edit_url',
                     render:
                        function (data, type, row, meta) {
                            return '<a href="'+data+
                            '"><img src="/++resource++unitracc-images/edit.png" alt="edit"></a>'
                        }
                     },
                    ],
            deferRender: true
        });
});""") % locals()

    @returns_json
    def review_data_json(self):
        """
        Daten für dataTable({ajax: {url, dataSrc: ''}})
        """
        context = self.context
        request = context.REQUEST
        review_state = request.get('review_state') or 'submitted'
        return jsonify(context,
                       self._getManagedContent(review_state),
                       raw=True)  # Verpackung durch den neuen Decorator

    def isDeveloper(self):
        """
        Darf der angemeldete Benutzer Entwicklerinformationen sehen?

        Es wird eine Berechtigung geprüft, keine Rolle; der Name wurde im Sinne
        der Handlichkeit gewählt.
        """
        cp = make_permissionChecker(self.context, verbose=debug_active)
        return cp(View_Development_Information)


# vim: ts=8 sts=4 sw=4 si et tw=79
