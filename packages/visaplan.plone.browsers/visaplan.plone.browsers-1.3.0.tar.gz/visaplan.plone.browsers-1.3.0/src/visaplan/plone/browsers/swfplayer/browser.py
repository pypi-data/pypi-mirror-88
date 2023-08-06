# Python compatibility:
from __future__ import absolute_import

# Zope:
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements

# Local imports:
from .config import HTML, SCRIPT


class ISWFPlayer(Interface):

    def get(prefix='', width='200', height='150', backgroundImage=''):
        """get player"""

    def getHTML(width='200', height='150', backgroundImage=''):
        """ """

    def getByBrain(width='200', height='150', backgroundImage=''):
        """ """


class Browser(BrowserView):

    implements(ISWFPlayer)

    def get(self, prefix='', width='200', height='150', backgroundImage=''):
        """ """
        context = self.context

        dict_ = {}
        dict_['width'] = width
        dict_['height'] = height

        if not prefix:
            prefix = 'swfplayer'

        dict_['id'] = prefix + '-' + context.UID()
        dict_['class'] = prefix
        dict_['backgroundImage'] = backgroundImage
        dict_['title'] = context.Title()
        dict_['description'] = context.Description()

        if not width:
            swfinfo = context.getAdapter('swfinfo')()
            dict_['width'] = swfinfo['width']
            dict_['height'] = swfinfo['height']

        if context.getContentType().startswith('video'):
            dict_['url'] = context.absolute_url() + '/@@flashfile/streamFlvFile/?.flv'
            return SCRIPT % dict_

        if context.getId().endswith('.flv'):
            dict_['url'] = context.absolute_url() + '/?.flv'
            return SCRIPT % dict_

        return ''

    def getHTML(self, width='200', height='150', backgroundImage=''):
        """ """
        context = self.context

        dict_ = {}
        dict_['width'] = width
        dict_['height'] = height

        dict_['backgroundImage'] = backgroundImage
        dict_['title'] = context.Title()
        dict_['description'] = context.Description()
        dict_['portalUrl'] = getToolByName(context, 'plone_portal_state').portal_url()

        if not width:
            swfinfo = context.getAdapter('swfinfo')()
            dict_['width'] = swfinfo['width']
            dict_['height'] = swfinfo['height']

        if context.getContentType().startswith('video'):
            dict_['url'] = context.absolute_url() + '/@@flashfile/streamFlvFile/?.flv'
            return HTML % dict_

        if context.getId().endswith('.flv'):
            dict_['url'] = context.absolute_url() + '/?.flv'
            return HTML % dict_

        return ''

    def getByBrain(self, brain, width='200', height='150', backgroundImage=''):
        """ """
        context = self.context
        if not backgroundImage:
            backgroundImage = 'swfplayer-background%s.png' % 200

        dict_ = {}
        dict_['width'] = width
        dict_['height'] = height

        dict_['backgroundImage'] = backgroundImage
        dict_['title'] = brain.Title
        dict_['description'] = brain.Description

        dict_['url'] = brain.getURL() + '/@@flashfile/streamFlvFile/?.flv'
        dict_['portalUrl'] = getToolByName(context, 'plone_portal_state').portal_url()

        return HTML % dict_
