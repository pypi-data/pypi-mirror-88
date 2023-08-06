# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

from six.moves import map

# visaplan:
from visaplan.plone.base.permissions import ManageGroups, ManageUsers
from visaplan.plone.breadcrumbs.base import (
    BaseCrumb,
    RootedCrumb,
    register,
    registered,
    )
from visaplan.plone.breadcrumbs.utils import crumbdict
# Nicht mehr nötig mit visaplan.plone.breadcrumbs 1+:
from visaplan.plone.browsers.management.oldcrumbs import imported
from visaplan.plone.tools.attools import getter_tuple
from visaplan.tools.minifuncs import translate_dummy as _

# Logging / Debugging:
from visaplan.tools.debug import pp


def user_label(key, hub, info):
    """
    Ermittle für den Benutzer, dessen ID durch die Request-Variable <key>
    angegeben ist, ein aussagekräftiges Label.

    Wenn nicht "beide Teile" vertreten sind (akademischer Titel und/oder
    Vorname, und Nachname), wird auch die User-ID verwendet.
    """
    user_id = info['request_var'].get(key)
    if not user_id:
        return None
    brain = hub['author'].getBrainByUserId(user_id)
    info['profile_brain'] = brain
    names = []
    part1, part2 = (False, False)
    for (aname, getter_name) in map(getter_tuple,
            ('academicTitle', 'firstname',
             )):
        val = getattr(brain, getter_name)
        if val:
            names.append(val)
            part1 = True
    for (aname, getter_name) in map(getter_tuple,
            ('lastname',
             )):
        val = getattr(brain, getter_name)
        if val:
            names.append(val)
            part2 = True
    name = ' '.join(names)
    if part1 and part2:
        return name
    elif name:
        return '%(name)s (%(user_id)s)' % locals()
    else:
        return user_id


class EditProfileSubcrumb(BaseCrumb):
    """
    Label wird gebildet aus Namensinformationen, ggf. ergänzt durch die
    Benutzer-ID;
    der Hyperlink verweist auf das Autorenprofil
    """
    def __init__(self, id=None, key='user_id', parents=[]):
        """
        key -- der Name der Request-Variablen
        """
        self._key = key
        BaseCrumb.__init__(self, id, parents)

    def tweak(self, crumbs, hub, info):
        key = self._key
        label = user_label(key, hub, info)
        if 0 and 'das funzt zwar offenbar, wird aber noch nicht verwendet':
            info['has_perm'][ManageUsers]
            # TODO: für Benutzermanager ein Krümel zur Benutzerverwaltung
            info['has_perm'][ManageGroups]
            info['has_perm']['Frobnosticate frosted froggies']
            info['has_perm']['Rule the world']
            pp(dict(info['has_perm']))
        if label is not None:
            url = info['profile_brain'].getURL()
            crumbs.append(crumbdict(
                label,
                '%(url)s/view'
                % locals()))


class ViewProfileSubcrumb(BaseCrumb):
    """
    Für Ansicht von Autorenprofilen:
    Benutzer-Manager sollen ein informatives Label und einen Link zum
    Benutzer-Management erhalten

    Achtung:
    Wegen des identischen Labels soll von dieser Klasse und EditProfileSubcrumb
    jeweils nur eines verwendet werden
    """
    def __init__(self, id=None, key='user_id', parents=[]):
        self._key = key
        BaseCrumb.__init__(self, id, parents)

    def tweak(self, crumbs, hub, info):
        key = self._key
        label = user_label(key, hub, info)
        if label is not None:
            url = info['profile_brain'].getURL()
            crumbs.append(crumbdict(
                label,
                '%(url)s/view'
                % locals()))


class GrouptitleCrumb(BaseCrumb):
    """
    Ein Krümel, der den Titel der durch eine Request-Variable angegebenen
    Gruppe ausgibt
    """
    def tweak(self, crumbs, hub, info):
        url = self._rooted_url(info, self.id)
        group_id = info['group_id']
        if group_id:
            crumbs.append(crumbdict(
                info['managed_group_title'],
                '%(url)s?group_id=%(group_id)s' % locals()
                ))


# -------------------------------------------- [ Initialisierung ... [
def register_crumbs():
    management_base_crumb = registered('management_view')
    for tid, label in [
        ('manage_users_view',
         _('User Management'),
         ),
        ('manage_groups_view',
         _('Groups Management'),
         ),
        ]:
        register(RootedCrumb(tid, label,
                             [management_base_crumb]))

    manage_users_crumb = registered('manage_users_view')
    for tid, label in [
        ('manage_users_add',
         _('Add user'),
         ),
        ('manage_users_delete',
         _('Delete users'),
         ),
        ('manage_users_lock',
         _('Lock users'),
         ),
        ('manage_users_unlock',
         _('Unlock users'),
         ),
        ('manage_duplicateprofiles_view',
         _('Cleanup duplicate profiles'),
         ),
        ]:
        register(RootedCrumb(tid, label,
                             [manage_users_crumb]))

    profile_crumb = register(EditProfileSubcrumb(None, 'user_id',
                             [manage_users_crumb]))
    for tid, label in [
        ('edit_group_membership',
         _('label_edit_group_memberships'),
         ),
        ]:
        register(RootedCrumb(tid, label,
                             [profile_crumb]))

    manage_groups_crumb = registered('manage_groups_view')
    for tid, label in [
        ('manage_group_add',
         _('Add group'),
         ),
        ]:
        register(RootedCrumb(tid, label,
                             [manage_groups_crumb]))

    group_details_crumb = register(GrouptitleCrumb('manage_group_details',
                                                   [manage_groups_crumb]))
    for tid, label in [
        ('manage_group_view',
         _('Group members'),
         ),
        ]:
        register(RootedCrumb(tid, label,
                             [group_details_crumb]))

register_crumbs()
# -------------------------------------------- ] ... Initialisierung ]

OK = True
