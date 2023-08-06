# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.breadcrumbs.base import RootedCrumb, register, registered
# Nicht mehr nötig mit visaplan.plone.breadcrumbs 1+:
from visaplan.plone.browsers.management.oldcrumbs import imported
from visaplan.tools.minifuncs import translate_dummy as _


# -------------------------------------------- [ Initialisierung ... [
def register_crumbs():
    management_base_crumb = registered('management_view')
    _page_id = 'order_management'
    order_management_crumb = RootedCrumb(_page_id,
                                  'Buchungsverwaltung',
                                  [management_base_crumb])
    register(order_management_crumb, _page_id)
    for tid, label in [
            ('order_add',
             _('Buchung hinzufügen'),
             ),
            ('order_edit',
             _('Buchung bearbeiten'),
             ),
            ('order_view',
             _('Buchung Detailansicht'),
             ),
            ]:
        register(RootedCrumb(tid, label,
                             [order_management_crumb]))


register_crumbs()
# -------------------------------------------- ] ... Initialisierung ]
