# -*- coding: utf-8 -*- äöü
"""
unitracc@@unitraccmail:utils
"""
# Python compatibility:
from __future__ import absolute_import

import six

# Standard library:
import re
from email.utils import formataddr, getaddresses

# visaplan:
from visaplan.tools.sequences import sequence_slide

__all__ = ['encodeHeaderAddress',
           'validateSingleEmailAddress',
           'emailListToString',
           'setHeaderOf',
           # nicht im Tomcom-Browser vorhanden:
           'harden_linebreaks',
           ]

# ------------------------------------------------------ [ Daten ... [
LINESEP = '\r\n'  # In Mails: immer, oder?
# ------------------------------------------------------ ] ... Daten ]

# -------------------------------------- [ aus tomcom.mail@@mail ... [
# -------------------------------------------- [ Daten ... [
EMAIL_RE = re.compile(r"^(\w&.%#$&'\*+-/=?^_`{}|~]+!)*[\w&.%#$&'\*+-/=?^_`{}|~]+@(([0-9a-z]([0-9a-z-]*[0-9a-z])?\.)+[a-z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$", re.IGNORECASE)
EMAIL_CUTOFF_RE = re.compile(r".*[\n\r][\n\r]")

EMAIL_ADDRESSES_RE = re.compile(r'(".*?" *|[^,^"^>]+?)(<.*?>)')
# -------------------------------------------- ] ... Daten ]

# ----------------------- [ ehemalige Browser-Methoden ... [
# ehemalige Browser-Methode _encodeHeaderAddress
def encodeHeaderAddress(address, charset):
    """
    address encoder

    Diese Doctests beschreiben den Status Quo:

    >>> encodeHeaderAddress(u'heinz@kunz', 'utf-8')
    u'heinz@kunz'
    >>> encodeHeaderAddress('heinz@kunz', 'utf-8')
    'heinz@kunz'
    """
    if address:
        return EMAIL_ADDRESSES_RE.sub(MailAddressTransformer(charset), address)

# ehemalige Browser-Methode _validateSingleEmailAddress
def validateSingleEmailAddress(address):
    """
    Validate a single email address, see also validateEmailAddresses

    Diese Doctests beschreiben den Status Quo:

    >>> validateSingleEmailAddress(None)
    False
    >>> validateSingleEmailAddress('heinz@kunz, brian@kohn')
    False
    >>> validateSingleEmailAddress('heinz@kunz')
    False
    >>> validateSingleEmailAddress('heinz@kunz.de')
    True
    """
    if not isinstance(address, six.string_types):
        return False

    sub = EMAIL_CUTOFF_RE.match(address)

    if sub != None:
        # Address contains two newlines (spammer attack using
        # "address\n\nSpam message")
        return False

    if len(getaddresses([address])) != 1:
        # none or more than one address
        return False

    # Validate the address
    for name, addr in getaddresses([address]):
        if not _validateSingleNormalizedEmailAddress(addr):
            return False
    return True

# ehemalige Browser-Methode _validateSingleNormalizedEmailAddress
def _validateSingleNormalizedEmailAddress(address):
    """Lower-level function to validate a single normalized email
    address, see validateEmailAddress
    """
    if not isinstance(address, six.string_types):
        return False

    sub = EMAIL_CUTOFF_RE.match(address)

    if sub != None:
        # Address contains two newlines (possible spammer relay attack)
        return False

    # sub is an empty string if the address is valid
    sub = EMAIL_RE.sub('', address)
    if sub == '':
        return True
    return False

# ehemalige Browser-Methode _emailListToString
def emailListToString(addr_list):
    """Converts a list of emails to rfc822 conforming data

    Input:
        ('email', 'email', ...)
    or
        (('name', 'email'), ('name', 'email'), ...)
    or mixed

    >>> emailListToString(['tobias@visaplan.com',
    ...                    ('Heinz Kunz', 'heinz@stein.de'),
    ...                    ])
    'tobias@visaplan.com, "Heinz Kunz" <heinz@stein.de>'

    Ein übergebener String wird nicht weiter geprüft:
    >>> emailListToString('%!$!!!')
    '%!$!!!'
    """
    # stage 1: test for type
    if not isinstance(addr_list, (list, tuple)):
        # a string is supposed to be a valid list of email addresses
        # or None
        return addr_list
    # stage 2: get a list of address strings using email.formataddr
    addresses = []
    for addr in addr_list:
        if isinstance(addr, six.string_types):
            addresses.append(formataddr(('', addr)))
        else:
            if len(addr) != 2:
                raise ValueError(
                    "Wrong format: ('name', 'email') is required")
            addresses.append(formataddr(addr))
    # stage 3: return the addresses as comma seperated string
    return ', '.join(addresses)

# ehemalige Browser-Methode _setHeaderOf
def setHeaderOf(msg, skipEmpty=False, **kwargs):
    """Set the headers of the email.Message based instance

    All occurences of the key are deleted first!
    """
    for key, val in kwargs.items():
        del msg[key]  # safe - email.Message won't raise a KeyError
        if skipEmpty and not val:
            continue
        msg[key] = val
    return msg

# ----------------------- ] ... ehemalige Browser-Methoden ]


class MailAddressTransformer:
    """ a transformer for substitution """

    def __init__(self, charset):
        self.charset = charset

    def __call__(self, matchobj):
        name = matchobj.group(1)
        address = matchobj.group(2)
        return str(email.Header.Header(name, self.charset)) + address
# -------------------------------------- ] ... aus tomcom.mail@@mail ]


def harden_linebreaks(s):
    r"""
    "Härte" die Zeilenumbrüche im übergebenen String gegen "Wegoptimierung"
    durch Outlook, und normalisiere sie

    >>> s = 'Zeile 1\nZeile 2\n\nZeile 3\r'
    >>> harden_linebreaks(s)
    'Zeile 1\t\r\nZeile 2\r\n\r\nZeile 3'
    >>> harden_linebreaks('Zeile 1\rZeile 2\n\nZeile 3\r')
    'Zeile 1\t\r\nZeile 2\r\n\r\nZeile 3'
    """
    res = []
    for tup in sequence_slide(s.splitlines()):
        prev, line, next = tup
        if (line and next
            and not line.endswith('\t')):
            line += '\t'
        res.append(line)
    return LINESEP.join(res)
