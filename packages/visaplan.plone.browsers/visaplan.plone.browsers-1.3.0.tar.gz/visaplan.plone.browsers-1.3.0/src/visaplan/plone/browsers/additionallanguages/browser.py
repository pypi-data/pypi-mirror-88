# Python compatibility:
from __future__ import absolute_import

# Standard library:
from types import ListType

# Zope:
from Products.Archetypes.annotations import AT_ANN_STORAGE, getAnnotation
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as pmf
from Products.Five import BrowserView
from zope.component import queryMultiAdapter
from zope.interface import Interface, implements

# Plone:
from plone.app.i18n.locales.browser.selector import LanguageSelector


class IAdditionalLanguagesInterFace(Interface):

    def getLanguages():
        """get available languages"""

    def getUsedLanguages():
        """get used languages"""

    def getAdditionalLanguages():
        """get additional languages"""

    def setAdditionalLanguages(value):
        """set additional languages"""

    def languages():
        """get languages"""

    def getTranslationUrlByLanguageCode(langCode):
        """give a code get an url"""

    def getLanguageCode():
        """get base language code"""

class Browser(BrowserView):
    implements(IAdditionalLanguagesInterFace)

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.lt = getToolByName(context, 'portal_languages', None)

    def getLanguageCode(self):
        """ """
        return self.context.REQUEST['LANGUAGE'][:2]

    def getLanguages(self):
        """ """
        list_ = []
        vorbidden_languages = [self.context.Language()]
        vorbidden_languages += list(self.context.getTranslations().keys())
        additionallanguages = self.getAdditionalLanguages()
        vorbidden_languages = [lang_code
                               for lang_code in vorbidden_languages
                               if lang_code not in additionallanguages]
        for lang_code in self.lt.getSupportedLanguages():
            lang_code = str(lang_code)
            if lang_code not in vorbidden_languages:
                list_.append((lang_code, self.lt.getNameForLanguageCode(lang_code)))
        return list_

    def getUsedLanguages(self):
        """ """
        context = self.context
        ann = getAnnotation(context)
        additionallanguages = ann.getSubkey(AT_ANN_STORAGE, subkey='AdditionalLanguages')
        if not additionallanguages:
            additionallanguages = []
        additionallanguages = list(additionallanguages)
        lang_code = context.Language()
        if not lang_code:
            lang_code = '_'
        additionallanguages.append(lang_code)
        if additionallanguages[1:] and additionallanguages.count('_'):
            additionallanguages.remove('_')
        return additionallanguages

    def getAdditionalLanguages(self):
        """ """
        context = self.context
        ann = getAnnotation(context)
        additionallanguages = ann.getSubkey(AT_ANN_STORAGE, subkey='AdditionalLanguages')
        if not additionallanguages:
            additionallanguages = []
        return additionallanguages

    def setAdditionalLanguages(self):
        """ """

        context = self.context
        additionallanguages = context.REQUEST.form.get('additionallanguages', [])
        if not isinstance(additionallanguages, list):
            additionallanguages = [additionallanguages]

        ann = getAnnotation(context)
        ann.setSubkey(AT_ANN_STORAGE, tuple(additionallanguages), subkey='AdditionalLanguages')
        context.invalidateTranslations()
        for lang_code, items in context.getTranslations().items():
            items[0].invalidateTranslations()
        context.reindexObject()

        pu = getToolByName(context, 'plone_utils')
        pu.addPortalMessage(pmf(u'Changes saved.'))

        context.REQUEST.RESPONSE.redirect(context.absolute_url()+'/view')

    def getTranslationUrlByLanguageCode(self, langCode):
        """ """
        if not hasattr(self.context, 'getTranslations'):
            translations = {}
        else:
            translations = self.context.getTranslations()

        if langCode in translations:
            trans = translations[langCode][0]
            state = queryMultiAdapter((trans, self.request),
                                      name='plone_context_state')
            return state.view_url() + '?set_language='+langCode
        return self.context.absolute_url() + '?set_language='+langCode

    def languages(self):
        """ """
        if self.lt is None:
            return []

        if not hasattr(self.context, 'getTranslations'):
            translations = {}
        else:
            translations = self.context.getTranslations()

        bound = self.lt.getLanguageBindings()
        current = bound[0]

        def merge(lang, info):
            info["code"] = lang
            if lang == current:
                info['selected'] = True
            else:
                info['selected'] = False
            return info

        results = [merge(lang, info)
                   for (lang, info) in self.lt.getAvailableLanguageInformation().items()
                   if info["selected"]]

        for data in results:
            data['translated'] = data['code'] in translations
            if data['translated']:
                trans = translations[data['code']][0]
                state = queryMultiAdapter((trans, self.request),
                                          name='plone_context_state')
                data['url'] = state.view_url() + '?set_language=' + data['code']
            else:
                state = queryMultiAdapter((self.context, self.request),
                                          name='plone_context_state')
                data['url'] = state.view_url() + '?set_language=' + data['code']

        return results
