# -*- coding: utf-8 -*-äöü  vim: ts=8 sts=4 sw=4 si et tw=79
"""\
unitracc@@changestate.utils
"""
# Python compatibility:
from __future__ import absolute_import

# Standard library:
from cgi import escape

# Zope:
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.tools.html import entity

# Local imports:
from .data import (
    _approval_level,
    _min_publication_level,
    _numeric_status_level,
    )

LISTPREFIX = u'%(bull)s%(nbsp)s' % entity

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import log_or_trace

logger, debug_active, DEBUG = getLogSupport(fn=__file__)


@log_or_trace(debug_active, logger=logger)
def is_publishing(context, transition):
    """
    - Ermittle den aktuellen Workflow-Status des Kontexts
    - Ermittle den Zielstatus
    - Ist der Zielstatus größer als der Ausgangsstatus?
      - Wenn ja:
        - wenn Zielstatus >= 'approved' ...
          - ... müssen eingebundene Objekte <= 'approved' auf ihren üblichen
            Veröffentlichungs-Level gehoben werden
          - müssen die im Temp-Ordner liegenden Objekte an ihre endgültigen
            Orte verschoben werden
      - Wenn nein, nimm keine Änderungen an eingebundenen Objekten vor

    Rückgabewert ist ein 2-Tupel (publishing, approving):

    - publishing ist True, wenn der Zielstatus größer als der alte und
      >= 'approved' ist; verwiesene Objekte müssen ggf. in die Mediathek
      verschoben werden
    - approving ist True, wenn der Zielstatus genau 'approved' ist.
      In diesem Fall wird die jeweilige Standard-Veröffentlichungsmethode
      gewählt.
    """
    pwt = getToolByName(context, 'portal_workflow')
    for wf in pwt.getWorkflowsFor(context):
        tdef = wf.transitions.get(transition, None)
        if tdef:
            sdef = wf._getWorkflowStateOf(context)
            old_status_id = sdef.getId()
            new_status_id = tdef.new_state_id
            old_state_level = _numeric_status_level[old_status_id]
            logger.info('  old level %r (%r)', old_status_id, old_state_level)
            new_state_level = _numeric_status_level[new_status_id]
            logger.info('  new level %r (%r)', new_status_id, new_state_level)
            return (new_state_level > old_state_level
                        and new_state_level >= _approval_level,
                    new_state_level == _approval_level,
                    )
    return (None, None)


def get_workflow_and_status(context, numeric=False):
    """
    Gib den konfigurierten Workflow sowie den aktuellen Workflow-Status des
    "Kontexts" (bzw. des übergebenen Objekts) zurück

    numeric -- wenn True, wird anstelle des String-Werts eine Zahl
               zurückgegeben, zwischen (derzeit) 10 (privat) und 120 (maximale
               Öffentlichkeit)

    siehe auch (gf):
    ../resolvereviewstate/browser.py
    """
    pwt = getToolByName(context, 'portal_workflow')
    for wf in pwt.getWorkflowsFor(context):
        sdef = wf._getWorkflowStateOf(context)
        logger.info('%(context)r: %(wf)r --> %(sdef)r', locals())
        old_status_id = sdef.getId()
        if numeric:
            return wf, _numeric_status_level[old_status_id]
        return wf, old_status_id
    return (None, None)


def get_workflow_status(context, numeric=False):
    """
    Gib den aktuellen Workflow-Status des "Kontexts" (bzw. des übergebenen
    Objekts) zurück

    numeric -- wenn True, wird anstelle des String-Werts eine Zahl
               zurückgegeben, zwischen (derzeit) 10 (privat) und 120 (maximale
               Öffentlichkeit)
    """
    return get_workflow_and_status(context, numeric)[1]


def make_reference_success_msg_html(liz, translate):
    """
    Erzeuge eine HTML-Nachricht;
    "Schwester-Funktion: --> make_reference_success_msg"
    """
    if not liz:
        return None  # pep 20.2
    cnt = len(liz)
    if cnt > 1:
        h2 = translate('${cnt} referenced objects processed:',
                       mapping=locals())
    else:
        h2 = translate('One referenced object processed:')
    txt = ['<div class="alert alert-info">'
           '<h2>', h2, '</h2>',
           '<ul>',
           ]
    for dic in liz:
        uid = dic['uid']
        o = dic['o']
        url = o.absolute_url_path()
        title = escape(o.title_or_id(), True)
        pt = translate(o.portal_type)
        txt.append('<li>'
                   '%(pt)s '
                   '<a href="%(url)s">%(title)s</a>'
                   '</li>'
                   % locals())
    txt.append('</ul>')
    txt.append('</div>')
    return ''.join(txt)


def make_reference_success_msg(liz, translate):
    """
    Erzeuge eine einfache Textnachricht
    """
    if not liz:
        return None  # pep 20.2
    cnt = len(liz)
    if cnt > 1:
        h2 = translate('${cnt} referenced objects processed:',
                       mapping=locals())
    else:
        h2 = translate('One referenced object processed:')
    txt = [h2]
    liz2 = []
    mask = LISTPREFIX + translate(
                    '%(pt)s "%(title)s"'
                    ' (/resolveuid/%(uid)s)')
    for dic in liz:
        uid = dic['uid']
        o = dic['o']
        pt = translate(o.portal_type)
        title = o.title_or_id()
        liz2.append(mask % locals())
    txt.append(', '.join(liz2))
    return '\n'.join(txt)


def make_reference_errors_msg(liz_nf, liz_errors, translate):
    """
    Erzeuge eine einfache Textnachricht
    """
    liz = list(liz_nf)
    liz.extend(liz_errors)
    if not liz:
        return None  # pep 20.2
    cnt = len(liz)
    if cnt > 1:
        h2 = translate('Errors during processing of ${cnt} referenced objects',
                       mapping=locals())
    else:
        h2 = translate('Errors during processing of referenced object')
    txt = [h2]
    if liz_nf:
        h3 = translate('Not found:')
        mask = LISTPREFIX + '%(uid)s'
        thelist = [mask % dic
                   for dic in liz_nf
                   ]
        txt.append('\n'.join((h3, '\n'.join(thelist))))
    if liz_errors:
        h3 = translate('Found but not processed:')
        thelist = []
        for dic in liz_errors:
            uid = dic['uid']
            o = dic['o']
            title = o.title_or_id()
            pt = translate(o.portal_type)
            mask = LISTPREFIX + translate(
                            '%(pt)s "%(title)s"'
                            ' (/resolveuid/%(uid)s)')
            thelist.append(mask % locals())
        txt.append('\n'.join((h3, '\n'.join(thelist))))
    return '\n'.join(txt)

def make_reference_errors_msg_html(liz_nf, liz_errors, translate):
    """
    Erzeuge eine HTML-Nachricht
    """
    liz = list(liz_nf)
    liz.extend(liz_errors)
    if not liz:
        return None  # pep 20.2
    cnt = len(liz)
    if cnt > 1:
        h2 = translate('Errors during processing of ${cnt} referenced objects',
                       mapping=locals())
    else:
        h2 = translate('Errors during processing of referenced object')
    txt = ['<div class="alert alert-error">'
           '<h2>', h2, '</h2>',
           '<ul>',
           ]
    if liz_nf:
        txt.extend(['<h3>',
                    translate('Not found:'),
                    '</h3>',
                    '<ul>',
                    ])
        for dic in liz_nf:
            txt.extend(['<li>'
                        '<tt>'
                        '<a href="/resolveuid/%(uid)s">%(uid)s</a>'
                        '</tt>'
                        '</li>'
                        % dic
                        ])
        txt.append('</ul>')

    if liz_errors:
        txt.extend(['<h3>',
                    translate('Found but not processed:'),
                    '</h3>',
                    '<ul>',
                    ])
        for dic in liz_errors:
            uid = dic['uid']
            o = dic['o']
            url = o.absolute_url_path()
            title = escape(o.title_or_id(), True)
            pt = translate(o.portal_type)
            txt.append('<li>'
                       '%(pt)s '
                       '<a href="%(url)s">%(title)s</a>'
                       '</li>'
                       % locals())
        txt.append('</ul>')
    txt.append('</div>')
    return '\n'.join(txt)
