# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.breadcrumbs.base import (
    BaseCrumb,
    RootedCrumb,
    register,
    registered,
    )
from visaplan.plone.breadcrumbs.utils import crumbdict
# Nicht mehr nötig mit visaplan.plone.breadcrumbs 1+:
from visaplan.plone.browsers.management.oldcrumbs import OK
from visaplan.tools.minifuncs import translate_dummy as _

try:
    # visaplan:
    from visaplan.plone.groups.groupdesktop.oldcrumbs import \
        OK  # Crumb: group_administration_view
    have_visaplan_groups = True
except ImportError:
    have_visaplan_groups = False
tan_management_crumbs = None  # verzögert


# ---------------------------------------------- [ Crumb-Klassen ... [
class TanManagementCrumbs(BaseCrumb):
    """
    Krümel für:
    - die Startseite der TAN-Verwaltung
    - ggf. die Unterseite für die Gruppe (ohne weitere Filter)
    """
    def tweak(self, crumbs, hub, info):
        url = self._rooted_url(info, self.id)
        crumbs.append(crumbdict(
            hub['translate']('TANs'),
            url))
        group_id = info['group_id']
        if group_id:
            crumbs.append(crumbdict(
                info['managed_group_title'],
                '%(url)s?group_id=%(group_id)s' % locals()
                ))


class CreateTanCrumb(BaseCrumb):
    """
    create_tan gibt es sowohl auf dem Gruppenschreibtisch
    als auch in der Unitracc-Verwaltung
    """

    def tweak(self, crumbs, hub, info):
        _ = hub['translate']

        gid = info['gid']
        if gid is not None:
            brain = info['desktop_brain']
            crumbs.append(crumbdict(_('Create TAN'),
                                    self._brain_id_and_gid(brain, gid)))
        else:
            tan_management_crumbs(crumbs, hub, info)
            crumbs.append(crumbdict(_('Create TAN'),
                                    self._rooted_url(info, self.id)))


class TanCrumbs(BaseCrumb):
    """
    Krümel für eine aktuell bearbeitete TAN.
    Ermittelt die Gruppen-ID und füttert das info-Dict. entsprechend;
    daher hier *Aufruf* der tan_management_crumbs,
    nicht eingebunden als parent.
    """
    def tweak(self, crumbs, hub, info):
        tan_info = hub['tan'].tan_info()
        if tan_info:
            info['group_id'] = tan_info['group_id']
            tan_management_crumbs(crumbs, hub, info)
            url = info['context_url']
            tan = tan_info['tan']
            tid = self.id
            crumbs.append(crumbdict(
                tan_info['Pretty_TAN'],
                '%(url)s/%(tid)s?tan=%(tan)s'
                % locals()))
        else:
            tan_management_crumbs(crumbs, hub, info)
# ---------------------------------------------- ] ... Crumb-Klassen ]


# -------------------------------------------- [ Initialisierung ... [
def register_crumbs():
    global tan_management_crumbs
    management_base_crumb = registered('management_view')
    tan_management_crumbs = register(
            TanManagementCrumbs('manage_tans',
                                [management_base_crumb]))
    register(TanCrumbs('manage_tan',
                       [management_base_crumb]))
    for tid, label in [
            ('manage_tan_status_summary',
             _('TAN status summary'),
             ),
            ('manage_tan_changesets',
             _('Last changes'),
             ),
            ('manage_redeemable_tans',
             _('Redeemable TANs'),
             ),
            ]:
        register(RootedCrumb(tid, label,
                             [tan_management_crumbs]))

    if have_visaplan_groups:
        # this is like we used to have it ...
        group_admin_crumb = registered('group_administration_view')
    else:
        # ... and this doesn't depend on visaplan.plone.groups
        group_admin_crumb = registered('manage_tan')
    register(CreateTanCrumb('create_tan',
                            parents=[group_admin_crumb]))

register_crumbs()
# -------------------------------------------- ] ... Initialisierung ]
