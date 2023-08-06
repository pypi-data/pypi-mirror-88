# -*- encoding: utf-8 -*- äöü
# Python compatibility:
from __future__ import absolute_import, print_function

from six.moves import filter

# Zope:
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.context import message

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport

logger, debug_active, DEBUG = getLogSupport('myaccount')


class IMyAccount(Interface):

    def set():
        """
        Speichere Änderungen des Profils
        """

    def get():
        """
        Gib ein Formular zur Änderung des Profils aus
        """

    def editProfile():
        """
        Alias für get
        """


class Browser(BrowserView):

    implements(IMyAccount)

    def set(self):
        """ """
        context = self.context
        getBrowser = context.getBrowser
        pm = getToolByName(context, 'portal_membership')
        if pm.isAnonymousUser():
            raise Unauthorized
        author = context.getBrowser('author').get()
        member = context.getBrowser('member')
        userId = member.getId()
        fullname = member.getFullname()

        request = context.REQUEST
        form = request.form

        if not getToolByName(context, 'portal_membership').checkPermission('Portlets: Manage portlets', context):
            form['suppress_portlet_management'] = True

        portal = getToolByName(context, 'portal_url').getPortalObject()
        sm = portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()
        try:

            errors = {}
            errors = author.validate(REQUEST=request, errors=errors, data=1, metadata=0)

            if errors:
                form['user_fullname'] = fullname  # Ansonsten wird oben in der top.pt "system" angezeigt
                form = context.restrictedTraverse('my_account_edit_form')(errors=errors, userId=userId)
                return form

            author.processForm()

        finally:
            sm.setOld()

        message(context,
                'Changes saved.')

        form['user_fullname'] = fullname
        desktop_path = context.getBrowser('unitraccfeature').desktop_path()
        return request.RESPONSE.redirect(portal.absolute_url() + desktop_path + '/@@myaccount/editProfile')

    def editProfile(self):
        """
        Gib ein Formular zur Bearbeitung des Profils des angemeldeten Benutzers aus
        """
        context = self.context

        if debug_active:
            def f(A):
                a = A.lower()
                for test in ('browser', 'portal', 'context',
                             ):
                    if test in a:
                        return True
                return False
        # Robuste Ermittlung des Kontexts:
        ok = False
        cnt = 0
        while True:
            cnt += 1
            try:
                getBrowser = context.getBrowser
                ok = True
            except AttributeError:
                context = context.getContext()
                getBrowser = context.getBrowser
                ok = True
            if debug_active:
                print(repr(context))
                print(list(filter(f, dir(context))))
            if ok or cnt >= 2:
                break

        request = context.REQUEST
        pm = getToolByName(context, 'portal_membership')
        if pm.isAnonymousUser():
            raise Unauthorized
        userId = context.getBrowser('member').getId()
        fullname = context.getBrowser('member').getFullname()
        management = context.getBrowser('management')
        if not management.canAccessSiteManagement():
            request.set('suppress_management_link', True)

        if not getToolByName(context, 'portal_membership').checkPermission('Portlets: Manage portlets', context):
            request.form['suppress_portlet_management'] = True

        portal = getToolByName(context, 'portal_url').getPortalObject()
        sm = portal.getAdapter('securitymanager')
        sm(userId='system')
        sm.setNew()

        try:
            request.form['user_fullname'] = fullname  # Ansonsten wird oben in der top.pt "system" angezeigt
            form = context.restrictedTraverse('my_account_edit_form')(userId=userId)
            return form
        finally:
            sm.setOld()

    get = editProfile
