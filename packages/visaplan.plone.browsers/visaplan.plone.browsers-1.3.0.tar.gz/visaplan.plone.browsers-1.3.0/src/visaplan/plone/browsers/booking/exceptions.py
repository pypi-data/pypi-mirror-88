# -*- coding: utf-8 -*- äöü
"""
Exception-Klassen für den booking-Browser
"""
# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.base.exceptions import (
    UidNotfoundException,
    UnitraccBaseException,
    )


class BookingException(UnitraccBaseException):
    pass

class MixedBookingException(BookingException):
    "Can't add %(title)s; mixed orders are not supported (%(oldval)s, %(newval)s)"
    mask_format = ("Can't add ${title}; "
                   "mixed orders are not supported"
                   " (${oldval}, ${newval})")
    def __init__(self, title, oldval, newval):
        UnitraccBaseException.__init__(self, title, oldval, newval)

class MixedVendorException(MixedBookingException):
    "Can't add %(title)s; mixed-vendor orders are not supported (%(oldval)s, %(newval)s)"
    mask_format = ("Can't add ${title}; "
                   "Mixed-vendor orders are not supported"
                   " (${oldval}, ${newval})")

class MixedCurrencyException(MixedBookingException):
    "Can't add %(title)s; mixed-currency orders are not supported (%(oldval)s, %(newval)s)"
    mask_format = ("Can't add ${title}; "
                   "Mixed-currency orders are not supported"
                   " (${oldval}, ${newval})")

class BookingConfigurationError(BookingException):
    pass

class MissingFallbackError(BookingConfigurationError):
    "Can't add %(title)s due to a missing %(key)r fallback value for language %(la)r"
    mask_format = ("Can't add ${title} "
                   "due to a missing ${key} fallback value for language ${la}")

class MissingValueError(BookingException):
    "Can't add %(title)s due to a missing %(key)r value"
    mask_format = ("Can't add ${title} "
                   "due to a missing ${key} value")
    def __init__(self, title, key):
        UnitraccBaseException.__init__(self, title, key)

class BookingProgrammingError(BookingException):
    "Booking error; if it persists, please call system administration"
    mask_format = __doc__
