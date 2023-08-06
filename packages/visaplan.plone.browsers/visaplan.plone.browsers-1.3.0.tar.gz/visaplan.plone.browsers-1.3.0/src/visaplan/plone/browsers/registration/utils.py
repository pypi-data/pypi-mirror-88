# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et tw=79

# Python compatibility:
from __future__ import absolute_import

from six.moves.urllib.parse import urlencode, urlsplit, urlunsplit

# Import schlaegt bei direkter Ausfuehrung leider fehl
# (bei Gelegenheit wieder testen):
# from visaplan.plone.browsers.tan.utils import tan2int, group3
# Daher hier simple Filterung - nur Dezimalziffern!


DIGITS = frozenset('0123456789')
def digitsonly(s):
    """
    >>> digitsonly('?earth=mostly&harmless')
    ''
    >>> digitsonly('123.456.789')
    '123456789'
    """
    return ''.join([ch for ch in s
                    if ch in DIGITS
                    ])


def stripped_ci_formvar(form, name):
    r"""
    Gib den Wert der übergebenen Formularvariablen zurück:
    - Der Variablenname wird ggf. auch in "kleinschreibung" probiert;
    - der Wert wird ggf. um äußeren Leerraum bereinigt zurückgeschrieben

    >>> form = {'dromedar': '  honk \t'}
    >>> stripped_ci_formvar(form, 'droMeDar')
    'honk'
    >>> form
    {'dromedar': 'honk'}
    """
    names = [name]
    names.extend(alternative_names(names))
    for name in names:
        if name in form:
            val = form[name].strip() or None
            form[name] = val
            return val
    return None  # pep 20.2


def alternative_names(liz):
    """
    Gib eine Liste mit alternativen Variablennamen zu den Namen in der Liste
    zurück.  Diese Liste kann leer sein, ebenso wie der Rückgabewert.

    >>> alternative_names(['initialTan', 'memberId'])
    ['initialtan', 'memberid']
    """
    res = []
    for name in liz:
        name2 = name.lower()
        if name2 not in liz and name2 not in res:
            res.append(name2)
    return res


def makeActivationLink(profile, portal, tan=None):
    """
    Gib einen Aktivierungslink zurueck

    >>> profile = MockProfile()
    >>> portal = MockPortal()
    >>> makeActivationLink(profile, portal)
    'http://test.me/@@registration/unlock?uid=abc123'
    >>> makeActivationLink(profile, portal, tan='123.456.789')
    'http://test.me/@@registration/unlock?uid=abc123&tan=123456789'
    >>> makeActivationLink(profile, portal, tan='?earth=mostly&harmless')
    'http://test.me/@@registration/unlock?uid=abc123'
    """
    su = list(urlsplit(portal.absolute_url()))
    # ['http', 'test.me', '/@@registration/unlock', 'uid=abc123&tan=123.456.789', '']
    su[2] = '/@@registration/unlock'
    qsl = [('uid', profile.UID())]
    if tan:
        try:
            tan = digitsonly(tan)
            if tan:
                qsl.append(('tan', tan))
        except ValueError:
            pass
    su[3] = urlencode(qsl)
    return urlunsplit(su)


def no_password_fieldname(s):
    """
    für dict-Filterung durch visaplan.tools.dicts.subdict

    >>> no_password_fieldname('userid')
    True
    >>> no_password_fieldname('password_confirm')
    False
    """
    return not 'password' in s


def get_hostname(request):
    """
    Extrahiere die Host-Information aus dem übergebenen Request
    und füge den Namen der verwendeten Variablen hinzu
    """
    for key in (
        'HTTP_X_FORWARDED_HOST',
        'ACTUAL_URL',
        'URL',
        'HTTP_HOST',
        ):
        val = request.get(key)
        if val:
            return '%(val)s  (%(key)s)' % locals()
    return None


def get_ip(request):
    """
    Extrahiere die Host-Information aus dem übergebenen Request
    und füge den Namen der verwendeten Variablen hinzu
    """
    for key in (
        'HTTP_X_FORWARDED_FOR',
        'REMOTE_ADDR',
        ):
        val = request.get(key)
        if val:
            return '%(val)s  (%(key)s)' % locals()
    return None


if __name__ == '__main__':
    # siehe auch ...tools.mock:
    class MockProfile:
        """
        nur zu Testzwecken
        """
        def UID(self):
            return 'abc123'

    class MockPortal:
        def absolute_url(self):
            return 'http://test.me'

    # Standard library:
    import doctest
    doctest.testmod()
