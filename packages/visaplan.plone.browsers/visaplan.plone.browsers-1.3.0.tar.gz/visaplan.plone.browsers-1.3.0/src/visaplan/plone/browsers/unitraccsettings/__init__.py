# Python compatibility:
from __future__ import absolute_import

# Zope:
from Products.CMFCore.permissions import setDefaultRoles

setDefaultRoles('settings: set', ('Manager',))
