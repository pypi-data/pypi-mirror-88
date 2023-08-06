# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.base.typestr import pluralize
from visaplan.plone.breadcrumbs.base import (
    BaseCrumb,
    ContextCrumb,
    RootedBrowserCrumb,
    RootedCrumb,
    RootedRequestvarCrumb,
    register,
    registered,
    )
from visaplan.plone.breadcrumbs.utils import crumbdict
from visaplan.tools.minifuncs import translate_dummy as _


# ---------------------------------------------- [ Crumb-Klassen ... [
class ManagementCenterCrumb(RootedBrowserCrumb):
    def __init__(self, id, parents=[]):
        RootedBrowserCrumb.__init__(self,
            id,
            label='Management',
            browser=None,
            parents=parents)

    def tweak(self, crumbs, hub, info):
        if info['management_center_done']:
            return
        RootedBrowserCrumb.tweak(self, crumbs, hub, info)
        info['management_center_done'] = True


class DetectGroupFromThread(BaseCrumb):
    """
    Erzeuge keinen eigenen Krümel, sondern ermittle die Gruppen-ID
    aus der Thread-ID *vor* dem Aufruf der Parents!

    Es wird allerdings der Gruppenschreibtischkrümel sichergestellt
    und der Gruppenforum-Krümel hinter diesen sortiert.
    """
    def __call__(self, crumbs, hub, info):
        if info['gid'] is None:
            tid = info['request_var'].get('tid')
            if tid is not None:
                info['gid'] = hub['groupboard'].get_group_id(tid)
        BaseCrumb.__call__(self, crumbs, hub, info)

    def tweak(self, crumbs, hub, info):
        tip = crumbs.pop()  # 'Gruppen-Forum' hier entfernen ...
        desktop_crumb = registered('group-desktop')
        if desktop_crumb:  # aus visaplan.plone.groups
            desktop_crumb(crumbs, hub, info, override=True)
        crumbs.append(tip)  # und nach dem Gruppenschreibtisch wieder anfügen


class BatchedCategoryCrumb(BaseCrumb):
    """
    Krümel für Suchergebnisseiten, der die Request-Variable "category" erhält.

    Wenn die Kategorie gefunden wird, wird dafür ein Krümel erzeugt;
    etwaige weitere Request-Variablen werden dem letzten vorherigen Krümel
    angehängt.
    """
    def tweak(self, crumbs, hub, info):
        category = info['request_var'].get('category')
        if category is not None:
            etype = hub['easyvoc'].getValue('unitracc-category', category)
            if etype:
                query = []
                for key in ('start', 'end', 'range'):
                    val = info['request_var'].get(key)
                    if val:
                        query.append((key, val))
                if query:
                    query_s = urlencode(query)
                    crumbs[-1]['href'] += '?' + query_s

                query.append(('category', category))
                url = info['context_url']
                query_s = urlencode(query)
                crumbs.append(crumbdict(
                    hub['translate'](pluralize(etype)),
                    '%(url)s?%(query_s)s' % locals()))
# ---------------------------------------------- ] ... Crumb-Klassen ]


# -------------------------------------------- [ Initialisierung ... [
def register_crumbs():
    management_base_crumb = ManagementCenterCrumb('management_view')
    register(management_base_crumb)

    """ Kopiervorlage:
    for tid, label in [
            ]:
        register(RootedBrowserCrumb(tid, label,
                                    None,
                                    [management_base_crumb]))

    """

    # ------ [ Direkte Kinder der Unitracc-Verwaltungsseite ... [
    for tid, label in [
            ('management_structure_elements',
             _('Manage structured contents'),
             ),
            ('review_submitted_content',  # ok
             _('Manage submitted content'),
             ),
            ('review_accepted_content',  # ok
             _('Manage accepted content'),
             ),
            ('pane_manage_locks',  # ?
             _('Lock Manager'),
             ),
            ('configure_rssfeed',
             _('Configure rss'),
             ),
            ('configure_stage',
             _('Configure stage'),
             ),
            ('pots_edit',
             _('Configure translations'),
             ),
            ('easyvoc_configure',  # ?
             _('Configure easyvoc vocabularies'),
             ),
            ('manage_vocabularies',  # ?
             _('Edit easyvoc vocabularies'),
             ),
            ('versioninformation_view',  # ok
             _('Version information'),
             ),
            ('unitraccfeature_view',  # ok
             _('Unitraccfeature view'),
             ),
            ('prefs_fckeditor_form',
             _('Configure editor'),
             ),
            ('fss_management_form',
             _('Configure file system storage'),
             ),
            ('configure_reply',
             _('Configure discussion'),
             ),

            ('order_management',  # ok
             _('Booking management'),
             ),
            ('manage_easyvoc',
             _('Vocabularies'),
             ),
            ]:
        register(RootedBrowserCrumb(tid, label,
                             None,
                             [management_base_crumb]))

    for tid, label in [
            ('plone_control_panel',
             _('Plone Configuration'),
             ),
            ('prefs_error_log_form',
             'heading_error_log',  # Default: 'Error log'
             ),
            ('manage_export_profiles',
             _('Export profiles'),
             ),
            ]:
        register(RootedCrumb(tid, label,
                             [management_base_crumb]))
    # ------ ] ... Direkte Kinder der Unitracc-Verwaltungsseite ]

    # ----------------------- [ Strukturelemente-Verwaltung ... [
    manage_structures_crumb = registered('management_structure_elements')
    for tid, label in [
            ('management_1255c69f5497ffb66ab21dfb9108ec4e_add',
             _('Vortrag hinzufügen'),
             ),
            ('management_1255c69f5497ffb66ab21dfb9108ec4e_copy',
             _('Vortrag kopieren'),
             ),
            ('management_1255c69f5497ffb66ab21dfb9108ec4e_publish',
             _('Presentations'),
             ),
            ('management_6c7879ebbc919b61c72f77a4a1d9474f_add',
             _('Skript hinzufügen'),
             ),
            ('management_6c7879ebbc919b61c72f77a4a1d9474f_copy',
             _('Skripte kopieren'),
             ),
            ('management_6c7879ebbc919b61c72f77a4a1d9474f_publish',
             _('Papers'),
             ),
            ('management_7dbcefcded46f02aa83458d8b13580be_add',
             _('Handlungsanweisung hinzufügen'),
             ),
            ('management_7dbcefcded46f02aa83458d8b13580be_copy',
             _('Handlungsanweisung kopieren'),
             ),
            ('management_7dbcefcded46f02aa83458d8b13580be_publish',
             _('Instructions'),
             ),
            ('management_86c045bc109c562f129be4ae034bf3cb_add',
             _('Fachinformationssystem hinzufügen'),
             ),
            ('management_86c045bc109c562f129be4ae034bf3cb_copy',
             _('Fachbuch kopieren'),
             ),
            ('management_86c045bc109c562f129be4ae034bf3cb_publish',
             _('Technical books'),
             ),
            ('management_9303f302674cb386293e2fa8ca46f7a3_add',
             _('Dokumentation hinzufügen'),
             ),
            ('management_9303f302674cb386293e2fa8ca46f7a3_copy',
             _('Dokumentationen kopieren'),
             ),
            ('management_9303f302674cb386293e2fa8ca46f7a3_publish',
             _('Documentations'),
             ),
            ]:
        register(RootedBrowserCrumb(tid, label,
                             None,
                             [manage_structures_crumb]))
    # ----------------------- ] ... Strukturelemente-Verwaltung ]

    # ------------------------ [ Plone-Konfigurationsseiten ... [
    control_panel_crumb = registered('plone_control_panel')
## Die Label hier sollen *nicht* vom Parser erfaßt werden,
## damit sie nicht überflüssigerweise in unitracc.pot
## auftauchen:
    for tid, label in [
            ('prefs_keywords_view',
             'Configure keywords',
             ),
            ('portal_registry',
             'Configuration registry',
             ),
            ]:
        register(RootedBrowserCrumb(tid,
                             label,
                             None,
                             [control_panel_crumb]))

    register(RootedRequestvarCrumb('prefs_error_log_showEntry',
                                   'id',
                                   [registered('prefs_error_log_form')]))

    for tid, label, browser in [
            ('syndication-settings',
             'Syndication',
             '',
             ),
            ('usergroup-groupprefs',
             'Groups',
             '',
             ),
            ('usergroup-controlpanel',
             'heading_usergroup_settings',  # Default: 'User/Group settings'
             '',
             ),
            # sofern nicht Suche statt Liste aktiviert ("Registration settings"),
            # leider sehr langsam; "Skipped user without principal object":
            ('usergroup-userprefs',
             'Users and Groups',
             '',
             ),
            ]:
        register(RootedBrowserCrumb(tid, label, browser,
                                    [control_panel_crumb]))
    # ------------------------ ] ... Plone-Konfigurationsseiten ]

    # -------------------------- [ Browser [tomcom.]easyvoc ... [
    for tid, label, browser in [
            ('member-registration',
             'Registration settings',  # oder label_member_registration
             ''),
            ]:
        register(RootedBrowserCrumb(tid, label, browser,
                 [registered('usergroup-controlpanel')]))
    for tid in [
            'easyvoc_edit',
            ]:
        register(RootedRequestvarCrumb(tid,
                                       'storage_key',
                                       [registered('manage_easyvoc')]))
    for tid, label in [
            ('configure_easyvoc',
             _('Add Vocabulary'),
             ),
            ]:
        register(RootedBrowserCrumb(tid,
                             label,
                             None,
                             [registered('manage_easyvoc')]))

    register(BatchedCategoryCrumb('event_folder_view'))
    # -------------------------- ] ... Browser [tomcom.]easyvoc ]

    for tid, label in [
        ('manage_translations_form',
         # 'header_manage_translations': in i18n-Domäne 'linguaplone'
         'Manage translations',
         ),
        ]:
        register(ContextCrumb(tid, label, []))

register_crumbs()
# -------------------------------------------- ] ... Initialisierung ]

OK = True
imported = True  # veraltet
