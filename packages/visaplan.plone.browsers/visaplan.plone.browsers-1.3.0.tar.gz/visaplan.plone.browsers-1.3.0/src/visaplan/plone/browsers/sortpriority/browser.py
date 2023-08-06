# Python compatibility:
from __future__ import absolute_import

# Zope:
from Products.Archetypes.utils import OrderedDict

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.context import getbrain

# TH: warum OrderedDict?
dict_ = OrderedDict()

dict_['partOf=technical_information_view'] = '0010-'
dict_['partOf=virtual_construction_view'] = '0020-'
dict_['partOf=documentation_view'] = '0030-'
dict_['UnitraccArticle'] = '0040-'
dict_['mediaFormat=x-shockwave-flash'] = '0050-'
dict_['mediaType=video'] = '0060-'
dict_['UnitraccImage'] = '0070-'
dict_['partOf=instructions_view'] = '0080-'
dict_['UnitraccNews'] = '0090-'
dict_['UnitraccTable'] = '0100-'
dict_['partOf=instructions_view'] = '0110-'
dict_['partOf=presentation_view'] = '0120-'
dict_['partOf=paper_view'] = '0130-'
dict_['UnitraccEvent'] = '0140-'
dict_['portal_type=UnitraccFormula'] = '0150-'
dict_['UnitraccStandard'] = '0160-'
dict_['UnitraccGlossary'] = '0170-'
dict_['x-shockwave-flash-sound'] = '0180-'
dict_['portal_type=UnitraccLiterature'] = '0190-'
dict_['UnitraccBinary'] = '0200-'
dict_['UnitraccAnimation'] = '0210-'
dict_['UnitraccAudio'] = '0220-'
dict_['UnitraccVideo'] = '0230-'


class ISortPriority(Interface):

    pass


class Browser(BrowserView):

    implements(ISortPriority)

    def __call__(self):
        """ """
        context = self.context

        if context.portal_type in dict_:
            return dict_[context.portal_type]

        if context.portal_type in ['Document']:
            uid = context.getHereAsBrain().getPartOf
            if uid:
                partOfBrain = getbrain(context, uid)
                if partOfBrain.getLayout == "book_agenda_view":
                    book = context.getBrowser('book')
                    partOfBrain = book.getBookFolderAsBrain(partOfBrain)
                return dict_['partOf=' + partOfBrain.getLayout]
        if context.portal_type in ['UnitraccFile']:
            mediaType, mediaFormat = context.getContentType().split('/')
            if 'mediaType=' + mediaType in dict_:
                return dict_['mediaType=' + mediaType]
            if 'mediaFormat=' + mediaFormat in dict_:
                return dict_['mediaFormat=' + mediaFormat]
            if 'partOf=' + context.getLayout() in dict_:
                return dict_['partOf=' + context.getLayout()]
            if 'portal_type=' + context.getGuessType() in dict_:
                return dict_['portal_type=' + context.getGuessType()]

        return ''
