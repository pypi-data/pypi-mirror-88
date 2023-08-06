# -*- coding: utf-8 -*- äöü
# Python compatibility:
from __future__ import absolute_import

from six.moves.urllib.request import urlopen

# Standard library:
from collections import defaultdict
from os.path import abspath, isdir, join, normpath, sep, split

# Zope:
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.plone.tools.cfg import get_config
from visaplan.tools.minifuncs import NoneOrString, makeBool

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport

logger, debug_active, DEBUG = getLogSupport()

# get_config erfordert die fn-Angabe noch:
_FACTORIES = defaultdict(lambda: NoneOrString)
# fn-Argument funktioniert in Entwicklungspaketen für diesen Zweck
# (noch?) nicht korrekt; daher product verwenden:
CONFIG = get_config(product='viewpreview',
                    defaults={
                        'dir': None,
                        'viewpreview_dir': None,
                        'urlmask_push': "http://pdfserver4.tcis.de/Add/URL/"
                                        "?response=push"
                                        "&URL=%(url)s/@@viewpreview/html"
                                        "?uid=%(uid)s"
                                        "&pushURL=%(url)s/@@viewpreview/save"
                                        "&token=%(uid)s"
                                        "&username=unitracc"
                                        "&width=880"
                                        "&output=jpg"
                        },
                    factories=_FACTORIES)


if CONFIG['dir'] is None:
    if CONFIG['viewpreview_dir'] is None:
        logger.warn('Unvollst. Konfiguration: %s', (CONFIG,))
        logger.warn('dir oder (alte Version) viewpreview_dir benoetigt!')
    CONFIG['dir'] = CONFIG.pop('viewpreview_dir', None)
elif CONFIG['viewpreview_dir'] is not None:
    if CONFIG['dir'] != CONFIG['viewpreview_dir']:
        logger.error('Konfiguration mismatch!'
                '\n            dir=%(dir)s;'
                '\nviewpreview_dir=%(viewpreview_dir)s',
                CONFIG)
        raise ValueError('Konfiguration')

if CONFIG['dir']:

    DIRNAME = abspath(CONFIG['dir'])
    if not isdir(DIRNAME):
        raise ValueError('Kein Verzeichnis %s gefunden! (%s)'
                         % (DIRNAME, CONFIG['dir']))


    def get_dir(check=True):
        """
        Gib das lokale Verzeichnis zur Speicherung der Vorschaubilder zurück
        """
        if check and not isdir(DIRNAME):
            raise ValueError('Kein Verzeichnis %s gefunden! (%s)'
                             % (DIRNAME, CONFIG['dir']))
        return DIRNAME
else:
    def get_dir(*args, **kwargs):
        """
        Dummy - we don't have a 'dir' product configuration value!
        """
        txt = ', '.join(args + [
                        '%s=%r' % tup
                        for tup in kwargs.items()
                            ])
        raise ValueError("get_dir(%(txt)s): We don't have a "
                         "[viewpreview ]dir product configuration value!"
                         % locals())


def get_filename(uid, check=True):
    """
    gib den Dateinamen für die Seite mit der übergebenen <uid> zurück
    """
    try:
        return join(get_dir(check), uid+'_ppt')
    except TypeError:
        logger.error('get_filename(%(uid)r, %(check)r)', locals())
        raise


def make_pushfunc(logger=logger, cfg=CONFIG):
    URLMASK = cfg['urlmask_push']
    if logger is not None:
        logger.info('URLMASK is %(URLMASK)s', locals())

    def pushfunc(**kwargs):
        """
        Push-funktion zum Anfordern eines Vorschaubilds.
        Benannte Argumente:

        uid - die UID; ggf. dem <context> entnommen
        url - die URL des (Unitracc-) Portals
        context - der Kontext
        logger - muß derzeit angegeben werden
        """
        context = kwargs.pop('context', None)
        uid = kwargs.pop('uid', None)
        if uid is None:
            uid = context.UID()
        logger = kwargs.pop('logger')
        logger.info('Requesting preview image for UID %(uid)r', locals())
        # an den Server zu übergebende URL:
        url = kwargs.pop('url', None)
        if url is None:
            portal = getToolByName(context, 'portal_url').getPortalObject()
            url = portal.absolute_url()
        cooked = URLMASK % locals()
        logger.info('Sending request to %(cooked)r', locals())
        OK = False
        try:
            with urlopen(cooked) as fp:
                data = fp.read()
                logger.info('Server answer: %(data)s', locals())
        except IOError as e:
            logger.error(str(e))
        except AttributeError as e:
            # "addinfourl instance has no attribute '__exit__'";
            # nur in vbox-therp, oder?
            logger.error(str(e))
        else:
            OK = True
        finally:
            if OK:
                logger.info('Expecting preview for UID %(uid)r',
                            locals())
            else:
                logger.error('Error requesting preview for UID %(uid)r',
                             locals())

    return pushfunc
