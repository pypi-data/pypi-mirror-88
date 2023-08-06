import pkg_resources
import pkg_resources

try:
    pkg_resources.get_distribution('zope.deprecation')
except pkg_resources.DistributionNotFound:
    'Imports from old location not supported'
else:
    from zope.deprecation import moved
    moved('visaplan.plone.browsers.booking.oldcrumbs', 'version 1.5')

