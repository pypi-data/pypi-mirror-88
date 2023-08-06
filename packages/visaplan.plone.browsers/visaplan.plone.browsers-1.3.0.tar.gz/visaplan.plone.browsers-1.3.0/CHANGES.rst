Changelog
=========


1.3.0 (2020-12-16)
------------------

Breaking changes:

- `.crumbs` modules renamed to `.oldcrumbs`.
  If zope.deprecation_ is installed, imports from the old location will continue
  to work until (including) version 1.4.x.

Improvements:

- Use visaplan.tools_.sql.subdict_ne
  (which sports the same order of source dict and fields spec
  as visaplan.tools.dicts.subdict)
  instead of visaplan.plone.sqlwrapper_.utils.extract_dict

- Replaced many uses of joined `getPhysicalPath` results
  by using the `getPath` method directly, which is supported by all
  catalog-aware objects.

Requirements:

- visaplan.tools_ v1.3.1+ (new `sql` module)

Requirements removed:

+-----------------------------+-----------------------+-----------------------+
| Package                     | Depending components  | Remarks               |
+=============================+=======================+=======================+
| visaplan.plone.breadcrumbs_ | several `oldcrumbs`   |                       |
|                             | modules               |                       |
+-----------------------------+-----------------------+-----------------------+
| visaplan.plone.groups_      | `oldcrumbs` modules of|                       |
|                             | browsers              |                       |
|                             | - `booking`           |                       |
|                             | - `management`        |                       |
|                             | - `tan` (access codes)|                       |
+-----------------------------+-----------------------+-----------------------+
| visaplan.plone.pdfexport_   |                       |                       |
+-----------------------------+-----------------------+-----------------------+
| visaplan.plone.sqlwrapper_  | Browsers              | Some of its functions |
|                             | - `booking`           | are in                |
|                             | - `tan` (access codes)| visaplan.tools_ now   |
|                             |                       | (since release 1.3.1) | 
+-----------------------------+-----------------------+-----------------------+
| visaplan.plone.structures   | Browsers              |                       |
|                             | - `changestate`       |                       |
|                             | - `servicetemp`       |                       |
|                             | - `xmlimport`         |                       |
|                             | Furthermore the       |                       |
|                             | structure element     |                       |
|                             | management facility of|                       |
|                             | the `management`      |                       |
|                             | browser (which are on |                       |
|                             | the list for          |                       |
|                             | refactoring anyway)   |                       |
+-----------------------------+-----------------------+-----------------------+
| visaplan.plone.unitracctool | Browsers              |                       |
|                             | - `author`            |                       |
|                             | - `registration`      |                       |
|                             | Furthermore the       |                       |
|                             | `.get_agb_link` method|                       |
|                             | of the `booking`      |                       |
|                             | browser will return   |                       |
|                             | `None`.               |                       |
|                             |                       |                       |
+-----------------------------+-----------------------+-----------------------+
| visaplan.UnitraccResource   | Some page templates use CSS an/or Javascript  |
|                             | resources provided by this package            |
+-----------------------------+-----------------------+-----------------------+
| Products.unitracc           | Browsers              | uses the              |
|                             | - `article`           | `SecurityContext`     |
|                             |                       | context manager (which|
|                             |                       | should be moved       |
|                             |                       | elsewhere)            |
+-----------------------------+-----------------------+-----------------------+
| latex2mathml_               | Browsers              |                       |
|                             | - `unitraccformula`   |                       |
+-----------------------------+-----------------------+-----------------------+
| tomcom.tcconvert            | Browsers              |                       |
|                             | - `unitraccaudio`     |                       |
|                             | - `unitraccvideo`     |                       |
|                             | - `unitraccvideomp4`  |                       |
|                             | - `unitraccvideoogg`  |                       |
+-----------------------------+-----------------------+-----------------------+

Thus, the `tan` browser e.g. (which provides an access codes facility)
will only be available if the visaplan.plone.groups_ package is installed.

If you need such optional functionality, please manage those optional packages
using e.g. your policy package or buildout script.

[tobiasherp]


1.2.4 (2020-08-12)
------------------

Bugfixes:

- unlock links didn't work (resulted in empty pages; HTTP status codes 204)

Miscellaneous:

- `@@registration` browser:

  - redirections now done by `Redirect` exceptions
  - logging for redirections
  - logging for transaction operations

[tobiasherp]


1.2.3 (2020-06-24)
------------------

Bugfixes:

- Copying of modules (presentations) didn't work, because of an empty selection list
  (if the modules have been moved to language-specific folders)

Improvements:

- Javascript file ``management_1255c69f5497ffb66ab21dfb9108ec4e_copy.js`` renamed to
  ``userselect-live-keypress.js``, because that is what it contains:

  - selection of a user, using
  - the deprecated jQuery ``.live`` method, and
  - keypress event handling ...

[tobiasherp]


1.2.2 (2020-06-12)
------------------

Miscellaneous:

- Template ``manage_export_profiles.pt`` removed;
  the correspondent skin layer template was used instead, anyway
  (from the visaplan.UnitraccSkins package; Rev. 31800)

- Some browsers removed from source
  (which had been taken out via ``MANIFEST.in`` for a while already):

  - now in visaplan.plone.elearning:

    - ``@@coursestatistics``
    - ``@@unitracccourse``
    - ``@@unitracccoursemanagement``

  - now in visaplan.plone.groups:

    - ``@@groupboard``
    - ``@@groupdesktop``
    - ``@@groupsharing``
    - ``@@unitraccgroups``

  - now in visaplan.plone.industrialsector:

    - ``@@industrialsector``

  - now in visaplan.plone.infohubs:

    - ``@@hubandinfo``

  - now in visaplan.plone.pdfexport:

    - ``@@export``

  - now in visaplan.plone.structures:

    - ``@@copystructure``
    - ``@@navigation``
    - ``@@presentation``
    - ``@@structureauthoring``
    - ``@@structurenumber``
    - ``@@structuretype``
    - ``@@temp``
    - ``@@tree``

  - now in visaplan.plone.transform:

    - ``@@transform``

- Usage of ``/@@resolveuid/`` instead of ``resolveUid`` in several places
- ``@@manage_users_view`` should be AJAX-loadable now

[tobiasherp]


1.2.1 (2020-04-07)
------------------

Improvements:

- The ``get_streaming_info`` methods
  of the unitraccaudio and unitraccvideo browsers
  yield only information about *existing* fields
  (since not all are guaranteed to exist anymore)

[tobiasherp]


1.2.0 (2020-04-03)
------------------

Improvements:

- Most configuration links on ``management_view`` already work now when loaded via AJAX
  (requires visaplan.plone.ajaxnavigation)

[tobiasherp]


1.1.4 (2020-03-06)
------------------

Breaking changes:

- Browser ``@@vcard``:

  - instead of ``UnitraccEvent.contact_name`` use ``ContactMixin.combinedContactName``
    (which is useful for list views as well)

  - Requires a ``Products.unitracc`` with the ``contact-metadata`` branch integrated.

Bugfixes:

- Double CSS class ``area-content`` in ``listing_nora.pt`` removed

Improvements:

- Python 3 compatibility (``python-modernize``)

Debugging code:

- Much debugging code removed or disabled

- excessive logging switched off in browsers

  - ``@@booking``
  - ``@@mainpage`` (logger.info() --> logger.debug())

- Some logging was added to

  - ``@@unitraccvideo``, because of video conversion
  - ``@@event``, because of an empty calendar

Miscellaneous:

- ``@@unitraccvideo`` browser does some debug logging

[tobiasherp]


1.1.3 (2019-12-18)
------------------

Bugfixes:

- Fixed a regression of ``manage_group_view`` in v1.1.2;
  the ``add_to_group`` method belongs to browser ``@@groupsharing``, not ``@@usermanagement``

- Fixed ``edit_group_membership``;
  the ``add_group_membership`` method belongs
  to browser ``@@groupsharing`` as well.

[tobiasherp]


1.1.2 (2019-12-06)
------------------

Bugfixes:

- Review view was broken

[tobiasherp]


1.1.1 (2019-12-05)
------------------

Improvements:

- The (non-public) ``@@management._getManagedContent`` method returns nothing older than 180 days by default
  (which makes the page load much faster)

Dependencies:

- visaplan.plone.tools_ v1.1.6+, because of ``@returns_json`` decorator

[tobiasherp]


1.1 (2019-11-28)
----------------

Improvements:

- Use new Javascript API; requires visaplan.UnitraccResource_ v1.1.0+
- ``manage_group_view`` initially sorts by `two` columns (`active` flag and name)
- Browser ``@@vcard``:

  - instead of ``UnitraccEvent.contact_name`` use ``ContactMixin.combinedContactName``
    (which is useful for list views as well)
  - Requires a ``Products.unitracc`` with the ``contact-metadata`` branch
    integrated (i.e., v3.1.5+)

New Features:

- `_embed` templates for AJAX navigation:

  - `nora_folder_embed`  (mixed news/articles view)

Requirements:

- Products.unitracc 3.1.5+

[tobiasherp]


1.0.7 (2019-06-26)
------------------

Improvements:

- `management_view`

  - convenience links to the Types tool and the `Folder` properties

- Allow for "system" user use when validating a structure (use Securitymanager)

Temporary change:

- Actions "Delete structure" and "Set subportal" disabled
  because they don't currently work (and need re-implementation)

[tobiasherp]


1.0.6 (2019-05-20)
------------------

Bugfixes:

- Translation for validation results

Improvements:

- for structure validation results:

  - Completion time and duration;
    localisation requires `Products.unitracc` 3.1.4.2+.

  - more useful links (contents and brain maintenance view)

  - preview image

- Lists of seekable Types: `FolderishAnimation` added (from `visaplan.plone.animations`)

[tobiasherp]


1.0.5 (2019-05-09)
------------------

Breaking changes:

- Structure management operations "delete structure" and "change subportal"
  are (most likely) broken; they'll need a little refactoring
  to work again (like was done for the structure validation already; see
  below).

Improvements for structure copy:

  - Use the same copy form and functionality for all types of structural content;
    requires `visaplan.plone.structures` v1.0.3.dev1+.

  - All fields of the copy form for structural content can be preset.

  - No clearing of the user_id filter "on click" anymore.

  - Selectable copy depth for refered objects (range 0 to 3, default: 2).

Improvements for structure management:

  - Unified form for all operstions (per structure type, for now)
    with inputs which are automatically shown/hidden, depending on the action

  - Structure validation now takes some parameters

  - Currently, the default action is "validation"

[tobiasherp]


1.0.4 (2019-03-22)
------------------

Breaking changes:

- Browsers `storagefolder` and `mediathek`
  moved to package `visaplan.plone.structures`
  (v1.0.2+)

- Browser `coursestatistics`
  moved to package `visaplan.plone.elearning`
  (v1.0.4+)

Cleanup:

- Browser `subportal` removed
  which had been removed from `configure.zcml` before (v1.0.2)

[tobiasherp]


1.0.3 (2019-02-14)
------------------

- Browser `industrialsector` moved to package `visaplan.plone.industrialsector`

- `self` arguments removed from interface methods (rev. 24965)

- Breadcrumb corrections for

  - `manage_export_profiles`
  - `order_management`

[tobiasherp]


1.0.2 (2019-01-31)
------------------

- Browser `subportal` moved to package `visaplan.plone.subportals`

- Browser `unitracctype`:

  - `getTypesForSearch` uses `portal_type` for videos and animations

- Bugfixes:

  - Editorial search for images didn't work

[tobiasherp]


1.0.2.dev1 (2018-10-12)
-----------------------

- Update of browser `nora` (News or Articles):
  Fixed News overview
  [tobiasherp]


1.0.1 (2018-09-26)
------------------

- more Browsers removed, which have been moved to `visaplan.plone.search` and `visaplan.plone.elearning`

- Bugfix: Imports from `visaplan.plone.industrialsector`

- Tools update
  [tobiasherp]


1.0 (2018-09-19)
----------------

First public release.

- Browser `unitraccfeature` removed
  (moved to `visaplan.plone.unitracctool`)

- Browsers `groupboard`, `groupdesktop`, `groupsharing`,
  `unitraccgroups` removed
  (moved to `visaplan.plone.groups`)

- more Browsers removed, which have been moved
  to `visaplan.plone.structures` and `visaplan.plone.industrialsector`
  [tobiasherp]

[tobiasherp]


.. _latex2mathml: https://pypi.org/project/latex2mathml
.. _visaplan.plone.breadcrumbs: https://pypi.org/project/visaplan.plone.breadcrumbs
.. _visaplan.plone.groups: https://pypi.org/project/visaplan.plone.groups
.. _visaplan.plone.pdfexport: https://pypi.org/project/visaplan.plone.pdfexport
.. _visaplan.plone.sqlwrapper: https://pypi.org/project/visaplan.plone.sqlwrapper
.. _visaplan.plone.tools: https://pypi.org/project/visaplan.plone.tools
.. _visaplan.tools: https://pypi.org/project/visaplan.tools
.. _visaplan.UnitraccResource: https://pypi.org/project/visaplan.UnitraccResource
.. _zope.deprecation: https://pypi.org/project/zope.deprecation
