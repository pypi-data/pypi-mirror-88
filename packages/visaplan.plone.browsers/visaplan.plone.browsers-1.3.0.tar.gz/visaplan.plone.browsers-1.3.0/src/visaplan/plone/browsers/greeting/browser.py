# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et tw=79
u"""\
Browser: Unitracc@@greeting - Grußformeln erzeugen
"""

# Python compatibility:
from __future__ import absolute_import, print_function

__author__ = "Tobias Herp <tobias.herp@visaplan.com>"

try:
    # visaplan:
    from visaplan.plone.base import BrowserView, Interface, implements
except ImportError:
    if __name__ == '__main__':
        class Interface(object):
            pass
        class BrowserView(object):
            pass
        def implements(*args, **kwargs):
            pass
    else:
        raise


class IGreeting(Interface):
    """
    Unitracc@@greeting - Grußformeln erzeugen (Interface)
    """

    def get(user=None, translate=None):
        u"""
        Gib die Anrede zurück für ... (Ideensammlung)

        - den übergebenen User
        - den User mit der übergebenen ID
        - den User zum übergebenen Profil
        - den User zum Profil aus dem Kontext
        """


class Browser(BrowserView):
    u"""
    Unitracc@@greeting - Grußformeln erzeugen
    """
    implements(IGreeting)

    def get(self, user=None, translate=None):
        u"""
        Gib die Anrede zurück für ... (Ideensammlung)

        - den übergebenen User
        - den User mit der übergebenen ID
        - den User zum übergebenen Profil
        - den User zum Profil aus dem Kontext

        translate -- die Funktion zur Übersetzung kann übergeben werden.
                     Wenn None, aber benötigt, wird der translate-Browser
                     verwendet; wenn 0, wird nicht übersetzt.
        """
        raise NotImplemented

if __name__ == '__main__':
    print(__doc__)
    print(IGreeting.__doc__)
    print(IGreeting.get.__doc__)
    print(Browser.__doc__)
    print(Browser.get.__doc__)
