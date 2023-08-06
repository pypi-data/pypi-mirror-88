# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.breadcrumbs.base import RootedCrumb, register, registered
from visaplan.plone.browsers.unitraccsettings.oldcrumbs import OK
from visaplan.tools.minifuncs import translate_dummy as _


# -------------------------------------------- [ Initialisierung ... [
def register_crumbs():
    settings_crumb = registered('manage_settings')
    _page_id = 'configure_registration'
    subportal_crumb = RootedCrumb(_page_id,
                                  _('Configure registration'),
                                  [settings_crumb])
    register(subportal_crumb, _page_id)

register_crumbs()
# -------------------------------------------- ] ... Initialisierung ]

OK = True
