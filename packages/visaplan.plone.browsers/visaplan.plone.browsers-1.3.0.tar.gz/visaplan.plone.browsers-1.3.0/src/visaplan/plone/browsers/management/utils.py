# -*- coding: utf-8 -*- äöü
# Python compatibility:
from __future__ import absolute_import

# Standard library:
from json import dumps as json_dumps

# Zope:
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.tools.context import make_timeFormatter, make_translator


def jsonify(context, brains, varname=None, raw=False):
    """
    Gib die übergebene Sequenz im JSON-Format zurück;
    ermittle zu diesem Zweck Informationen, die ansonsten beim Rendern durch
    TAL beschafft würden (was aber - bei langen Listen - sehr (!) lang dauert)
    """
    res = []
    _ = make_translator(context)  # ggf. auch den Import wieder löschen
    pm = getToolByName(context, 'portal_membership')
    format_time = make_timeFormatter(context, True)

    getMember = pm.getMemberById
    for brain in brains:
        creator_id = brain.Creator
        creator_o = getMember(creator_id)
        creator_exists = creator_o is not None
        if creator_exists:
            creator_name = creator_o.getProperty('fullname', creator_id)
        else:
            creator_name = creator_id + ' (not found)'
        url = brain.getURL()
        dic = {'title': brain.Title,
               'view_url': url and (url+'/view'),
               'edit_url': url and (url+'/edit'),
               # 'creator_id': creator_id,
               'creator_name': creator_name,
               'modification_time': format_time(brain.modified),
               'portal_type': _(brain.portal_type),
               }
        res.append(dic)
    if raw:
        return res
    if varname:
        return '\n%s = %s;' % (varname, json_dumps(res))
    return json_dumps(res)
