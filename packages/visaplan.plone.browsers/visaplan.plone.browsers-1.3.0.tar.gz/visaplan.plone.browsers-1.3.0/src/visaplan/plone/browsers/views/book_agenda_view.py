# -*- coding: utf-8 -*-

# Python compatibility:
from __future__ import absolute_import

# Zope:
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# visaplan:
from visaplan.plone.browsers import _


class BookAgendaView(BrowserView):
    template = ViewPageTemplateFile('book_agenda_embed.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.msg = _(u'A small message')
        return self.template()
