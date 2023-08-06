# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=0
# Python compatibility:
from __future__ import absolute_import

# 3rd party:
from latex2mathml.converter import convert

# visaplan:
from visaplan.plone.base import BrowserView, Interface, implements

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport

logger, debug_active, DEBUG = getLogSupport(fn=__file__)

# TODO: Funktion zur Reparatur der unverdaulichen MathML-Darstellungen
#       ("alte, i.e. aus Unitracc 1.0 migrierte Formeln"
#       mit nicht deklariertem m:-Namensraum)
# from .utils import fix_namespace


class IUnitraccFormula(Interface):

    def get(brain=None, string_=''):
        """Return the formula depending of the type with
           a special leading sign. This is necessary for mathjax
        """


class Browser(BrowserView):

    implements(IUnitraccFormula)

    def get(self, brain=None, string_=''):


        if not string_:
            if not brain:
                context = self.context
                string_ = context.getXml()
            else:
                string_ = brain.getXml

        # Q&D-Erkennung von MathML:
        if string_.startswith('<math'):
            return string_

        # "alte Formeln"; TODO: korrigieren, s.o.
        if string_.startswith('<m:math'):
            if brain:
                liz = [brain, 'Brain']
            else:
                if 'context' not in locals():
                    context = self.context
                liz = [context, 'context']
            liz.append(string_[:30])
            logger.warning('%r (%s): Veraltete Formel (%r)', *tuple(liz))
            return string_

        # andernfalls TeX annehmen:
        logger.info('konvertiere: %r%s', string_[:30], string_[30:] and '...' or '')
        try:
            return convert(string_)
        except Exception as e:  # (TypeError, ValueError, IndexError) ...
            # wie provoziert man mit einem String einen Konversionsfehler?
            liz = [string_]
            if brain:
                liz.append(brain)
            else:
                if 'context' not in locals():
                    context = self.context
                liz.append(context)
            logger.error('Kann %r nicht konvertieren (%r)', *tuple(liz))
            logger.exception(e)
            kw = {'messageType': 'error',
                  'message': 'Error converting TeX formula',
                  'errcls': e.__class__.__name__,
                  'errtext': str(e),
                  'errdetails': string_,
                  'errdetails_label': 'LaTeX text',
                  }
            return context.restrictedTraverse('msgbox')(**kw)
