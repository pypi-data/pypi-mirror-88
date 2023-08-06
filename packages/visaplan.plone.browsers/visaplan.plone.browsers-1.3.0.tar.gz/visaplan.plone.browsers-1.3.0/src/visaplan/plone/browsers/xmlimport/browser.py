# -*- coding: utf-8 -*- äöü
"""
Created on 04.11.2013

@author: enrico

Not-yet-replaced adapters:
- normalize (tomcom.adapter)
- createobject (tomcom.adapter)
"""
# Python compatibility:
from __future__ import absolute_import

from six import string_types as six_string_types

# Standard library:
from collections import defaultdict
from xml.etree.cElementTree import ParseError

# Zope:
import transaction
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.base.typestr import pt_string
from visaplan.plone.tools.context import \
    message  # requires context 1st argument
from visaplan.tools.classes import SetterDict

# Local imports:
from .fileprocessor import Fileprocessor

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport

logger, debug_active, DEBUG = getLogSupport()


DEBUG = 0
if DEBUG:
    # Logging / Debugging:
    from pdb import set_trace

class IXMLImport(Interface):
    """
    Interface zur Klasse MultiUpload
    """

    def processForm():
        """
         - Annehmen der Formulardaten
         - Validierung des Formulars
         - Weiterreichen an passenden Typen
        """

    def _handleGlossary_():
        """
        Speichern der Inhalte in der ZODB
        dict_of_values = Felderwerte
        """

    def _handleArticles_():
        """
        Speichern der Inhalte in der ZODB
        dict_of_values = Felderwerte
        """

    def _handleNews_():
        """
        Speichern der Inhalte in der ZODB
        dict_of_values = Felderwerte
        """

    def _handleEvents_():
        """
        Speichern der Inhalte in der ZODB
        dict_of_values = Felderwerte
        """

    def canImport(portal_type):
        """
        Darf der angemeldete Benutzer den uebergebenen Typ importieren?
        """

    def authImport(portal_type):
        """
        Wirft ggf. Unauthorized
        """


# erforderliche Felder:
required_fields = defaultdict(lambda: ['title', 'content'])
required_fields['UnitraccEvent'] = required_fields['UnitraccGlossary'] + ['start']
# "zusätzliche Felder":
optional_fields = defaultdict(lambda: ['description', 'publish', 'language'])
optional_fields['UnitraccEvent'] = optional_fields['UnitraccGlossary'] + \
        ['end', 'location',
         'street', 'city', 'zip', 'country',
         ]

def handlerArgs(typ):
    """
    gib anhand der defaultdicts required_fields und optional_fields die
    Werte zurück, die zum Aufruf von parseXML für den übergebenen Typ
    verwendet werden müssen.

    Rückgabewert: ein dict
    """
    fields = set(required_fields[typ])
    opt = set(optional_fields[typ])
    optionalfields = opt.difference(fields)
    return {'fields': fields,
            'optionalfields': optionalfields,
            }


class Browser(BrowserView):
    '''
    classdocs
    '''

    implements(IXMLImport)


    def processForm(self):
        """
         - Annehmen der Formulardaten
         - Validierung des Formulars
         - Weiterreichen an passenden Typen
        """
        context = self.context
        portal = getToolByName(context, 'portal_url').getPortalObject()
        form = self.context.REQUEST.form
        content_type = form.get('content_type')
        gid = form.get('unitraccGroups', [])
        if not form.get('cancel'):
            elements, errors = self._handle(content_type)
            handled = False
            if isinstance(errors, str):
                msg = errors
                handled = True
            elif elements:
                msg = '%d elements in xml found. ' % (len(errors) + elements)
                msg += '%d elements saved. ' % elements
            elif not elements and errors:
                msg = '%d elements in xml found. ' % (len(errors) + elements)
                msg += '%d valid elements found. ' % elements
            elif not form.get('file'):
                msg = "No File found."
            else:
               msg = '%d elements in xml found.' % (len(errors) + elements)

            message(context, msg)

            if errors and not handled:
                for error in errors:
                    errormsg = error + "!"
                    message(context, errormsg, 'error')

        desktop_path = context.getBrowser('unitraccfeature').desktop_path()
        if gid:
            tmpl = '%s?gid=%s' % (pt_string[content_type]['our-thingies'], gid[0])
        else:
            tmpl = pt_string[content_type]['my-thingies']
        return context.REQUEST.response.redirect(portal.absolute_url()
                                                 + '/'.join((desktop_path,
                                                             tmpl)))

    def canImport(self, portal_type):
        """
        Darf der angemeldete Benutzer den uebergebenen Typ importieren?
        """
        context = self.context
        if not isinstance(portal_type, six_string_types):
            logger.error('%(context)r.canImport: portal_type is not a string (%(portal_type)r)',
                         locals())
            return False
        checkperm = getToolByName(context, 'portal_membership').checkPermission
        if not checkperm('unitracc: Import XML', context):
            return False
        if not checkperm('unitracc: Import %s' % portal_type, context):
            return False
        if not checkperm('unitracc: Add %s' % portal_type, context):
            return False
        return True

    def authImport(self, portal_type):
        """
        Wirft ggf. Unauthorized
        """
        if not self.canImport(portal_type):
            raise Unauthorized

    def _handle(self, typ):
        """
        Generische Methode zum Import von XML-Daten

        typ -- z. B. 'UnitraccGlossary', 'UnitraccEvent'

        Rückgabewert: ein 2-Tupel mit
        - Anzahl der importierten Objekte
        - Liste der Fehler
        """
        data = self.context.REQUEST.form
        xmlfile = data.get('file')
        if not xmlfile:
            return 0, []
        w3l = data.get("w3l", False)
        kwargs = handlerArgs(typ)
        # Parsen des XML Dokuments
        try:
            objects, errors = Fileprocessor.parseXML(kwargs['fields'],
                                                 kwargs['optionalfields'],
                                                 xmlfile,
                                                 w3l)
        except ParseError as e:
            objects = []
            errors = "XML-Document invalid!"

        # Speichern der Objekte
        for o in objects:
            self._saveObject_(typ, o,
                              data['workflow'])
        return len(objects), errors

    def _handleGlossary_(self):
        """
        verarbeiten der Daten aus Formular und parsen des XML
        """
        return self._handle('UnitraccGlossary')

    def _handleArticles_(self):
        """
        Speichern der Inhalte in der ZODB
        dict_of_values = Felderwerte
        """
        return self._handle('UnitraccArticles')

    def _handleNews_(self):
        """
        Speichern der Inhalte in der ZODB
        dict_of_values = Felderwerte
        """
        return self._handle('UnitraccNews')

    def _handleEvents_(self):
        """
        Speichern der Inhalte in der ZODB
        dict_of_values = Felderwerte
        """
        return self._handle('UnitraccEvent')

    def _saveObject_(self, portal_type, element, workflow):
        """
        portal_type -- der Typ des neuen Elements
        element -- das Elementobjekt

        """
        global DEBUG
        if DEBUG:
            set_trace()
        context = self.context
        form = context.REQUEST.form
        group_ids = form.get('unitraccGroups', None)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        temp = context.getBrowser('temp')
        tempfolder = temp.getTempFolder()
        create = tempfolder.getAdapter('createobject')
        user_id = context.getBrowser('member').getId()
        normalize = context.getAdapter('normalize')

        title = element['title']
        # Erstelle neues Objekt in tempfolder
        new_object = create(portal_type, normalize(title))

        # Setze den Besitzer
        changeowner = new_object.getBrowser('changeowner')
        changeowner.set(user_id)

        # Setze Inhalte
        # new_object.setTitle(title)
        # new_object.setDescription(element.pop('description'))
        # new_object.setText(element.pop('content'))

        for (key, val) in element.items():
            if val:
                aname = setter[key]
                a = getattr(new_object, setter[key])
                if callable(a):
                    a(val)
                else:
                    a = val

        if hasattr(new_object, '_at_creation_flag'):
            delattr(new_object, '_at_creation_flag')
            new_object._p_changed = 1

        if group_ids:
            new_object.addUnitraccGroups(group_ids)

        # neuer Workflow-Status
        new_object.getBrowser('workflow')\
                    .change('make_' + workflow)

        transaction.commit()

        if workflow == 'public':
            mediathek = portal.getBrowser('mediathek')
            mediathek.move(new_object)
        rc = getToolByName(context, 'reference_catalog')
        new_object = rc.lookupObject(new_object.UID())
        new_object.reindexObject()
        return True


setter = SetterDict()
setter['publish'] = 'setEffectiveDate'
setter['content'] = 'setText'
