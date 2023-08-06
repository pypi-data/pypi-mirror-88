# -*- coding: utf-8 -*- äöü
"""
Browser unitracc@@contenticon: Ermittle ein Icon für den Inhaltstyp (für Suchergebnisse)
"""
# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements
from visaplan.plone.tools.context import getbrain
from visaplan.tools.classes import Proxy


class IContentIcon(Interface):

    def get(brain):
        """
        Gib einen Icon-Pfad zurück

        - für eine Auswahl von Typen: das Piktogramm für diesen Typ
        - für Dateien: Differenzierung nach Inhaltstyp, z. B. Videos und Animationen
        - ansonsten nach Layout, z. B. technical_information_folder_view
        """

WHITELIST = ['UnitraccArticle',
             'UnitraccNews',
             'UnitraccImage',
             'UnitraccTable',
             'UnitraccEvent',
             'UnitraccAuthor',
             ]
rootpath = 'code'
ICONMASK = '%(rootpath)s/icon_%%(pt)s.png' % locals()
PICTOMASK = '%(rootpath)s/picto_%%s.png' % locals()


def tup2path(tup):
    """
    Ordne einem 2-Tupel aus portal_type und (opt). contentType einen Pfad zu
    """
    pt, ct = tup
    # portal_type --> Bildpfad
    if pt in WHITELIST:
        return ICONMASK % (locals())
    if ct is None:
        return None
    # contentType --> Bildpfad
    if ct == 'application/x-shockwave-flash':
        return PICTOMASK % 'animation'
    if ct.startswith('video'):
        return PICTOMASK % 'video'
    if ct.endswith('html'):
        return ICONMASK % {'pt': pt+'_html'}
    return None  # pep 20.2


MAP = Proxy(tup2path)


class Browser(BrowserView):

    implements(IContentIcon)

    def get(self, brain):
        """
        Gib einen Icon-Pfad zurück
        """
        pt = brain.portal_type
        pa = MAP[(pt, None)]
        if pa is not None:
            return pa
        pa = MAP[(pt, brain.getContentType)]
        if pa is not None:
            return pa
        uid = brain.getPartOf
        if uid:
            context = self.context
            folderBrain = getbrain(context, uid)
            return ICONMASK % {'pt': folderBrain.getLayout}
        return None  # pep 20.2

        # Alter, nunmehr toter Code:
        if brain.portal_type in WHITELIST:
            return '/code/icon_' + brain.portal_type + '.png'
        if brain.portal_type == 'UnitraccFile':
            if brain.getContentType.startswith('video'):
                return '/code/picto_video.png'
            if brain.getContentType == 'application/x-shockwave-flash':
                return '/code/picto_animation.png'

            if brain.getContentType.endswith('html'):
                return '/code/icon_' + brain.portal_type + '_html.png'

        uid = brain.getPartOf
        if uid:
            context = self.context
            folderBrain = getbrain(context, uid)
            return '/code/icon_' + folderBrain.getLayout + '.png'
