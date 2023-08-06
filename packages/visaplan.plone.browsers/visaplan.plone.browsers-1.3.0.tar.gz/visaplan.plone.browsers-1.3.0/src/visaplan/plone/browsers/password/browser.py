# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=79
# Python compatibility:
from __future__ import absolute_import

# Zope:
from AccessControl import Unauthorized
from App.config import getConfiguration
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.base.exceptions import (
    EmptyPassword,
    InvalidPassword,
    PasswordTooShort,
    )
from visaplan.plone.tools.context import make_translator, message
from visaplan.tools.minifuncs import translate_dummy as _

conf = getConfiguration()
env = conf.environment
MINIMUM_PASSWORD_LENGTH = env.get('MINIMUM_PASSWORD_LENGTH', 5)
try:
    MINIMUM_PASSWORD_LENGTH = int(MINIMUM_PASSWORD_LENGTH)
except ValueError:
    MINIMUM_PASSWORD_LENGTH = 5

if 0 and 'Futter fuer den Parser':
    _('Empty password is not allowed.')
    _('Password is too short; at least %(minlength)r characters required.')
    _('The new password and the repetition are not the same.')


class IPassword(Interface):

    def change():
        """ """

    def validate(password, translate):
        """
        pruefe den uebergebenen Wert auf Zulaessigkeit als Passwort
        und wirf ggf. einen ValueError
        """


class Browser(BrowserView):

    implements(IPassword)

    def change(self):
        """ """
        context = self.context
        form = context.REQUEST.form

        # check permission:
        if not getToolByName(context, 'portal_membership').checkPermission('Set own password', context):
            raise Unauthorized

        password = form.get('password', '')
        passwordValidation = form.get('passwordValidation', '')

        error = False
        try:
            translate = make_translator(context)
            self.validate(password, translate)
        except InvalidPassword as e:
            error = True
            message(context, str(e), 'error')
        else:
            if password != passwordValidation:
                error = True
                message(context, _('The new password and the repetition are not the same.'),
                        'error')

        if not error:
            memberId = context.getBrowser('member').getId()
            acl = getToolByName(context, 'acl_users')
            acl.userSetPassword(memberId, password)

            message(context, _('Changes saved.'))

        return context.REQUEST.RESPONSE.redirect(context.REQUEST['HTTP_REFERER'])

    def validate(self, password, translate):
        """
        pruefe den uebegebenen Wert auf Zulaessigkeit als Passwort
        und wirf ggf. einen ValueError
        """
        global MINIMUM_PASSWORD_LENGTH
        if not password:
            raise EmptyPassword(translate)
        length = len(password)
        if length < MINIMUM_PASSWORD_LENGTH:
            raise PasswordTooShort(translate, MINIMUM_PASSWORD_LENGTH)
