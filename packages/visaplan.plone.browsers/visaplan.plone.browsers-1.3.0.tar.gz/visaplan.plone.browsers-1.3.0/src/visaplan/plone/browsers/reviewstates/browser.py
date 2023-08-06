# Python compatibility:
from __future__ import absolute_import

# Zope:
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements


class IReviewStates(Interface):

    def get():
        """ """


class Browser(BrowserView):

    implements(IReviewStates)

    def get(self):
        """ """
        context = self.context
        pw = getToolByName(context, 'portal_workflow')
        list_ = []
        for review_state in ['published',
                             'inherit',
                             'visible',
                             'restricted',
                             'private']:
            dict_ = {}

            dict_['title'] = pw['dayta_workflow'].states[review_state].title
            dict_['id'] = review_state

            list_.append(dict_)
        return list_

    def getFCKList(self):
        """ """
        # siehe (gf) ../unitraccsearch/browser.py, getReviewStates
        context = self.context
        pw = getToolByName(context, 'portal_workflow')
        list_ = []
        for review_state in ['published',
                             'inherit',
                             'visible',
                             'accepted',
                             'submitted',
                             'private']:
            dict_ = {}

            dict_['title'] = pw['dayta_workflow'].states[review_state].title
            dict_['id'] = review_state

            list_.append(dict_)
        return list_
